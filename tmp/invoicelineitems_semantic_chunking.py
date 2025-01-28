import os
import psycopg2
import json
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import re
from datetime import datetime

# Parameters to be replaced in api
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
DOC_INTELLIGENCE_ENDPOINT = os.getenv("DOC_INTELLIGENCE_ENDPOINT")
DOC_INTELLIGENCE_KEY = os.getenv("DOC_INTELLIGENCE_KEY")
POSTGRESQL_CONNECTION = os.getenv("POSTGRESQL_CONNECTION")

# Initialize Clients
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
document_analysis_client = DocumentAnalysisClient(
    endpoint=DOC_INTELLIGENCE_ENDPOINT,
    credential=AzureKeyCredential(DOC_INTELLIGENCE_KEY)
)

# PostgreSQL Connection
conn = psycopg2.connect(POSTGRESQL_CONNECTION)

def download_blob(container_name, blob_name):
    """Download a blob from Azure Blob Storage."""
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    return blob_client.download_blob().readall()

def analyze_document(document_data):
    """Extract text and structure using Azure AI Document Intelligence."""
    poller = document_analysis_client.begin_analyze_document(
        model_id="prebuilt-document",
        document=document_data
    )
    result = poller.result()
    
    chunks = []
    invoice_number = None
    in_table = False

    # Define regex patterns
    invoice_number_pattern = re.compile(r'Invoice Number:\s*(\S+)')
    due_date_pattern = re.compile(r'Due Date:\s*(\d{4}-\d{2}-\d{2})')
    line_item_pattern = re.compile(r'(?P<deliverable>[\w\s]+)\s+\$(?P<amount>[\d,]+.\d{2})')

    for page in result.pages:
        for line in page.lines:
            text = line.content
            print(f"Processing text: {text}")  # Debugging

            # Search for the Invoice number in the text
            if not invoice_number:
                match = invoice_number_pattern.search(text)
                if match:
                    invoice_number = match.group(1)
                    print(f"Found Invoice number: {invoice_number}")  # Debugging

            # Search for the Due Date in the text
            due_date_match = due_date_pattern.search(text)
            due_date = due_date_match.group(1) if due_date_match else None

            # Detect the start of the table
            if "Deliverables" in text and "Amount" in text:
                in_table = True
                continue

            # Process table rows
            if in_table:
                line_item_match = line_item_pattern.search(text)
                if line_item_match:
                    chunks.append({
                        "deliverable": line_item_match.group('deliverable').strip(),
                        "amount": float(line_item_match.group('amount').replace(',', '')),
                        "due_date": due_date
                    })
                else:
                    # End of table
                    in_table = False

    return chunks, invoice_number

def insert_chunks_to_db(chunks, invoice_number, conn):
    """
    Insert the chunks into the database.
    """
    cursor = conn.cursor()
    # Fetch the invoice_id based on the invoice number
    cursor.execute("SELECT id FROM invoices WHERE number = %s", (invoice_number,))
    invoice_id = cursor.fetchone()
    
    if invoice_id:
        invoice_id = invoice_id[0]
    else:
        raise ValueError(f"Invoice number '{invoice_number}' not found in the invoices table.")
    
    for chunk in chunks:
        # Determine the status based on the due date
        status = 'Completed' if chunk['due_date'] and datetime.strptime(chunk['due_date'], '%Y-%m-%d') < datetime(2024, 12, 31) else 'Pending'
        cursor.execute(
            """
            INSERT INTO invoice_line_items (invoice_id, description, amount, status, due_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (invoice_id, chunk['deliverable'], chunk['amount'], status, chunk['due_date'])
        )
    conn.commit()
    cursor.close()

def process_document(container_name, blob_name, conn):
    """
    Process an invoice: download, analyze via Document Intelligence, chunk and insert data into the database.
    """
    
    # Download the document
    document_data = download_blob(container_name, blob_name)

    print(f"Processing document {document_data} from container {container_name}...")

    # Analyze the document to extract chunks and invoices number
    chunks, invoices_number = analyze_document(document_data)

    # Insert the chunks into the database
    insert_chunks_to_db(chunks, invoices_number, conn)

# Example usage
if __name__ == "__main__":
    container_name = "documents"
    blob_names = ["INV-TWC2024-001.pdf"]  # List of blob names to process

    conn = psycopg2.connect(POSTGRESQL_CONNECTION)

    try:
        for blob_name in blob_names:
            process_document(container_name, blob_name, conn)
    finally:
        # Close the database connection
        conn.close()