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
        print(f"Found invoice number: {invoice_number}") # Debugging
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
            due_date_field = item.value.get("DueDate")

            # Extract and clean up fields
            description = description_field.content if description_field else "N/A"
            amount = amount_field.content if amount_field else "0"
            # Remove currency symbols or extra characters from amount
            amount = float(re.sub(r"[^\d.]", "", amount))
            due_date = due_date_field.content if due_date_field else "1970-01-01"

            line_items.append({
                "description": description,
                "amount": amount,
                "due_date": due_date
            })

    return invoice_number, line_items

# Download the document data from blob storage
container_name = "documents"
blob_name = "INV-TWC2024-001.pdf"
document_data = download_blob(container_name, blob_name)

# Extract line items from the document data
invoice_number, line_items = extract_invoice_line_items(document_data)
print(line_items)


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
        """, (1,item['description'], item['amount'], 'Pending', item['due_date']))

    conn.commit()
    cursor.close()
    conn.close()

# Insert the extracted line items with the fetched invoice_id
insert_line_items_to_db(invoice_number, line_items)






# # Analyze document and store chunks
# def process_document(container_name, blob_name, conn):
#     """Complete workflow for processing a document."""
#     print(f"Processing document {blob_name} from container {container_name}...")
    
#     # Download the document data
#     document_data = download_blob(container_name, blob_name)

#     # Analyze the document to extract chunks and INV number
#     chunks, invoice_number = analyze_document(document_data)
#     print(f"Document analyzed. Chunks: {chunks}, Invoice Number: {invoice_number}") # Debugging
    
#     # Insert the chunks into the database
#     insert_chunks_to_db(chunks, invoice_number, conn)

# # Example usage
# if __name__ == "__main__":
#     container_name = "documents"
#     blob_names = ["INV-TWC2024-001.pdf"]  # List of blob names to process

#     conn = psycopg2.connect(POSTGRESQL_CONNECTION)

#     try:
#         for blob_name in blob_names:
#             process_document(container_name, blob_name, conn)
#     finally:
#         # Close the database connection
#         conn.close()
