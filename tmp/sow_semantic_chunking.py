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
    current_heading = None
    sow_number = None

    # Regex pattern for the SOW number
    sow_number_pattern = re.compile(r'SOW Number:\s*(SOW-\S+)')

    for page in result.pages:
        for line in page.lines:
            text = line.content
            print(f"Processing text: {text}") # Debugging
            if is_heading(text, known_headings):  # Detect headings 
                current_heading = text
                chunks.append({"heading": text, "content": "", "page_number": page.page_number})
            elif current_heading:
                chunks[-1]["content"] += " " + text  # Add text to the last chunk

            # Search for the SOW number in the text
            if not sow_number:
                match = sow_number_pattern.search(text)
                if match:
                    sow_number = match.group(1)
                    print(f"Found SOW number: {sow_number}") # Debugging
    return chunks, sow_number

# List of known headings
known_headings = [
    "Project Scope", "Project Objectives", "Location", "Tasks", "Schedules",
    "Standards and Testing", "Payments", "Compliance", "Requirements", "Project Deliverables"
]

def is_heading(text, known_headings):
    # Check if the text matches any known headings
    if text.strip() in known_headings:
        return True
    
    return False
    #return text.strip().endswith(":") or text.strip().isdigit() or text.lower().startswith("section")

def insert_chunks_to_db(chunks, sow_number, conn):
    cursor = conn.cursor()
    # Fetch the sow_id based on the SOW number
    cursor.execute("SELECT id FROM sows WHERE number = %s", (sow_number,))
    sow_id = cursor.fetchone()
    
    if sow_id:
        sow_id = sow_id[0]
    else:
        raise ValueError(f"SOW number '{sow_number}' not found in the sows table.")
    
    for chunk in chunks:
        cursor.execute("""
            INSERT INTO sow_chunks (sow_id, heading, content, page_number)
            VALUES (%s, %s, %s, %s)
        """, (sow_id, chunk['heading'], chunk['content'], chunk['page_number']))
    
    conn.commit()
    cursor.close()
    conn.close()


# Analyze document and store chunks
def process_document(container_name, blob_name, conn):
    """Complete workflow for processing a document."""
    print(f"Processing document {blob_name} from container {container_name}...")
    
    # Download the document data
    document_data = download_blob(container_name, blob_name)
    
    # Analyze the document to extract chunks and SOW number
    chunks, sow_number = analyze_document(document_data)
    
    # Insert the chunks into the database
    insert_chunks_to_db(chunks, sow_number, conn)

# Example usage
if __name__ == "__main__":
    container_name = "documents"
    blob_names = ["Statement_of_Work_TailWind_Cloud_Solutions_Woodgrove_Bank_20241101.pdf"]  # List of blob names to process

    conn = psycopg2.connect(POSTGRESQL_CONNECTION)

    try:
        for blob_name in blob_names:
            process_document(container_name, blob_name, conn)
    finally:
        # Close the database connection
        conn.close()
