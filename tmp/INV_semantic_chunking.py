import os
import re
from datetime import datetime
import psycopg2
import json
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

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
    """Download a blob from Azure Blob Storage."""
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    return blob_client.download_blob().readall()
    

def extract_invoice_line_items(document_data):
    """Extract line items from the invoice using Azure AI Document Intelligence."""  
    poller = document_analysis_client.begin_analyze_document(
        model_id="prebuilt-invoice", 
        document=document_data
    )
    result = poller.result()

    # Ensure there's at least one document in the result
    if not result.documents:
        raise ValueError("No documents were found in the analysis result.")
    
    invoice_number = None

    # Regex pattern for the invoice number
    invoice_number_pattern = re.compile(r'Invoice Number:\s*(INV-\S+)')

    # Extract text content from the result
    text = ""
    for page in result.pages:
        for line in page.lines:
            text += line.content + "\n"

    # Search for the invoice number in the text
    match = invoice_number_pattern.search(text)
    if match:
        invoice_number = match.group(1)
    else:
        raise ValueError("Invoice number not found in the document.")

    # Extract line items from the first document
    line_items = []
    invoice = result.documents[0]  # Assuming a single invoice document
    items_field = invoice.fields.get("Items")
    if items_field and items_field.value:
        for item in items_field.value:
            description_field = item.value.get("Description")
            amount_field = item.value.get("Amount")
            due_date_field = item.value.get("Date")

            # Extract and clean up fields
            description = description_field.content if description_field else "N/A"
            amount = amount_field.content if amount_field else "0"
            
            # Remove currency symbols or extra characters from amount
            amount = float(re.sub(r"[^\d.]", "", amount))
            due_date = due_date_field.content if due_date_field else "1970-01-01"

            # Determine the status based on the due date
            status = 'Completed' if due_date and datetime.strptime(due_date, '%Y-%m-%d') < datetime(2024, 12, 31) else 'Pending'  # Changed line
            print(f"Inserting chunk: {description}, {amount}, {due_date}, {status}") # Debugging

            line_items.append({
                "description": description,
                "amount": amount,
                "due_date": due_date,
                "status": status
            })

    return invoice_number, line_items


def insert_line_items_to_db(invoice_number, line_items):
    # Establish database connection
    cursor = conn.cursor()

    # Fetch the invoice_id based on the invoice number
    cursor.execute("SELECT id FROM invoices WHERE number = %s", (invoice_number,))
    invoice_id = cursor.fetchone()
    
    if invoice_id:
        invoice_id = invoice_id[0]
    else:
        raise ValueError(f"Invoice number '{invoice_number}' not found in the invoices table.")

    # Insert each line item into the database
    for item in line_items:
        cursor.execute("""
            INSERT INTO invoice_line_items (invoice_id,description, amount, status, due_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (1,item['description'], item['amount'], item['status'], item['due_date']))

    conn.commit()
    cursor.close()
    conn.close()

# Download the document data from blob storage
container_name = "documents"
blob_name = "INV-TWC2024-001.pdf"
document_data = download_blob(container_name, blob_name)

# Extract line items from the document data
invoice_number, line_items = extract_invoice_line_items(document_data)

# Insert the extracted line items with the fetched invoice_id
insert_line_items_to_db(invoice_number, line_items)