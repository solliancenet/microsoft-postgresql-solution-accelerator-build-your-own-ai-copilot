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

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

document_analysis_client = DocumentAnalysisClient(
    endpoint=DOC_INTELLIGENCE_ENDPOINT,
    credential=AzureKeyCredential(DOC_INTELLIGENCE_KEY)
)

# PostgreSQL Connection
conn = psycopg2.connect(POSTGRESQL_CONNECTION)

def download_blob(container_name, blob_name):
    # Implement the logic to download the blob from Azure Blob Storage
    # This is a placeholder implementation
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_data = blob_client.download_blob().readall()
    return blob_data

def is_heading(text, known_headings):
    return text.strip() in known_headings

# List of known headings
known_headings = [
     "Deliverables", "Amount", "Due Date"
]


def analyze_document(document_data):
    # Analyze the document using Azure Form Recognizer
    poller = document_analysis_client.begin_analyze_document("prebuilt-layout", document_data)
    result = poller.result()

    chunks = []
    current_heading = None
    invoice_number = None

    # Regex pattern for the invoice number
    invoice_number_pattern = re.compile(r'Invoice Number:\s*(INV-\S+)')

    for page in result.pages:
        for line in page.lines:
            text = line.content.strip()
            print(f"Processing text: {text}") # Debugging
            if is_heading(text, known_headings):  # Detect headings 
                current_heading = text
                chunks.append({"heading": text, "content": "", "page_number": page.page_number})
                print(f"New heading detected: {current_heading}") # Debugging
            elif current_heading:
                chunks[-1]["content"] += " " + text  # Add text to the last chunk
                print(f"Appending to chunk: {chunks[-1]}") # Debugging

            # Search for the invoice number in the text
            if not invoice_number:
                match = invoice_number_pattern.search(text)
                if match:
                    invoice_number = match.group(1)
                    print(f"Found invoice number: {invoice_number}") # Debugging

    # Process the chunks to extract table rows
    extracted_data = []
    deliverables, amounts, due_dates = [], [], []
    for chunk in chunks:
        if chunk['heading'] == 'Deliverables':
            deliverables = chunk['content'].split()
        elif chunk['heading'] == 'Amount':
            amounts = chunk['content'].split()
        elif chunk['heading'] == 'Due Date':
            due_dates = chunk['content'].split()

    for deliverable, amount, due_date in zip(deliverables, amounts, due_dates):
        extracted_data.append({
            'deliverable': deliverable,
            'amount': amount,
            'due_date': due_date
        })

    return extracted_data, invoice_number

def insert_chunks_to_db(chunks, invoice_number, conn):
    """
    Insert the chunks into the database.
    """
    cursor = conn.cursor()
    try:
        # Fetch the invoice_id based on the invoice number
        cursor.execute("SELECT id FROM invoices WHERE number = %s", (invoice_number,))
        invoice_id = cursor.fetchone()
        
        if invoice_id:
            invoice_id = invoice_id[0]
        else:
            raise ValueError(f"Invoice number '{invoice_number}' not found in the invoices table.")
        
        for chunk in chunks:
            # Determine the status based on the due date
            status = 'Completed' if chunk['due_date'] and datetime.datetime.strptime(chunk['due_date'], '%Y-%m-%d') < datetime.datetime(2024, 12, 31) else 'Pending'
            print(f"Inserting chunk: {chunk}") # Debugging
            cursor.execute(
                """
                INSERT INTO invoice_line_items (invoice_id, description, amount, status, due_date)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (invoice_id, chunk['deliverable'], chunk['amount'], status, chunk['due_date'])
            )
        conn.commit()
        print("Chunks inserted successfully") # Debugging
    except Exception as e:
        print(f"Error inserting chunks to DB: {e}") # Debugging
        conn.rollback()
    finally:
        cursor.close()

def process_document(container_name, blob_name, conn):
    print(f"Processing document: {blob_name}") # Debugging
    document_data = download_blob(container_name, blob_name)
    print(f"Document data downloaded: {document_data}") # Debugging
    
    # Analyze the document to extract chunks and INV number
    chunks, invoice_number = analyze_document(document_data)
    print(f"Document analyzed. Chunks: {chunks}, Invoice Number: {invoice_number}") # Debugging
    
    # Insert the chunks into the database
    insert_chunks_to_db(chunks, invoice_number, conn)

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
        print("Database connection closed") # Debugging