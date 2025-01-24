
import os
import psycopg2
import json
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import re
from datetime import datetime

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
DOC_INTELLIGENCE_ENDPOINT = os.getenv("DOC_INTELLIGENCE_ENDPOINT")
DOC_INTELLIGENCE_KEY = os.getenv("DOC_INTELLIGENCE_KEY")
POSTGRESQL_CONNECTION = os.getenv("POSTGRESQL_CONNECTION")
BLOB_BASE_URL = os.getenv("BLOB_BASE_URL")

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
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    download_stream = blob_client.download_blob()
    return download_stream.readall()

def extract_text_from_document(document_data):
    """Extract text and structure using Azure AI Document Intelligence."""
    poller = document_analysis_client.begin_analyze_document(
        model_id="prebuilt-document",
        document=document_data
    )
    result = poller.result()
    extracted_text = []
    for page in result.pages:
        page_text = " ".join([line.content for line in page.lines])
        extracted_text.append(page_text)
    return extracted_text

def parse_extracted_text(extracted_text, document_url):
    """Parse the extracted text to get the required values for the invoices table."""
    # Initialize the invoice data dictionary
    invoice_data = {
        'number': None,
        'vendor': None,
        'amount': None,
        'invoice_date': None,
        'payment_status': 'Pending',  # Default value
        'document': document_url,  # Insert the full blob details
        'metadata': extracted_text,
        'embeddings': None
    }

    # Define regex patterns for extracting information
    number_pattern = re.compile(r'Invoice Number:\s*(\S+)')
    amount_pattern = re.compile(r'Total Amount[:\s]+[$]?([\d,]+(?:\.\d{1,2})?)', re.IGNORECASE)
    date_pattern = re.compile(r'Invoice Date:\s*(\d{4}-\d{2}-\d{2})')
    vendor_pattern = re.compile(r'Vendor:\s*([^\n]+)')

    # Iterate over the extracted text to find matches
    full_text = ' '.join(extracted_text)
    
    number_match = number_pattern.search(full_text)
    if number_match:
        invoice_data['number'] = number_match.group(1)

    amount_match = amount_pattern.search(full_text)
    if amount_match:
        invoice_data['amount'] = float(amount_match.group(1).replace(",", ""))

    date_match = date_pattern.search(full_text)
    if date_match:
        invoice_data['invoice_date'] = date_match.group(1)

    vendor_match = vendor_pattern.search(full_text)
    if vendor_match:
        vendor_name = vendor_match.group(1).strip()
        # Extract only the vendor name part
        vendor_name = vendor_name.split(' Address:')[0]
        invoice_data['vendor'] = vendor_name
  
    # Check if all required fields are extracted
    if not all([invoice_data['number'], invoice_data['vendor'], invoice_data['amount'], invoice_data['invoice_date']]):
        raise ValueError("Failed to extract all required fields from the document.")

    return invoice_data

def insert_invoice_to_db(invoice_data, conn):
    """Insert invoice data into the PostgreSQL database."""
    cursor = conn.cursor()
    
    # Fetch the vendor_id based on the vendor name
    cursor.execute("SELECT id FROM vendors WHERE name = %s", (invoice_data['vendor'],))
    vendor_id = cursor.fetchone()
    
    if vendor_id:
        vendor_id = vendor_id[0]
    else:
        raise ValueError(f"Vendor '{invoice_data['vendor']}' not found in the vendors table.")

    insert_query = """
    INSERT INTO invoices (number, vendor_id, amount, invoice_date, payment_status, document, metadata, embeddings)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(insert_query, (
        invoice_data['number'],
        vendor_id,
        invoice_data['amount'],
        invoice_data['invoice_date'],
        invoice_data['payment_status'],
        invoice_data['document'],
        json.dumps(invoice_data['metadata']),  # Convert metadata to JSON string
        invoice_data['embeddings']
    ))

    conn.commit()
    cursor.close()
    #conn.close()

def process_document(container_name, blob_name, document_id,conn):
    """Complete workflow for processing a document."""
    print(f"Processing document {document_id} from container {container_name}...")
   
    document_data = download_blob(container_name, blob_name)
    document_url = f"{BLOB_BASE_URL}/{container_name}/{blob_name}"
    extracted_text = extract_text_from_document(document_data)
    invoice_data = parse_extracted_text(extracted_text, document_url)
    insert_invoice_to_db(invoice_data, conn)
    

# Example usage

if __name__ == "__main__":
    container_name = "documents"
    blob_names = ["INV-TWC2024-001.pdf","INV-TWC2024-002.pdf","INV-TWC2024-003.pdf","INV-TWC2024-004.pdf", "INV-TWC2024-005.pdf"] # List of blob names to process

    conn = psycopg2.connect(POSTGRESQL_CONNECTION)

    try:
        for blob_name in blob_names:
            document_id = blob_name.replace(".pdf", "")
            process_document(container_name, blob_name, document_id, conn)
    finally:
        # Close the database connection
        conn.close()