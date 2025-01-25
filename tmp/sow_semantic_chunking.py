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

def analyze_document(file_path):
    with open(file_path, "rb") as file:
        poller = document_analysis_client.begin_analyze_document("prebuilt-layout", document=file)
        result = poller.result()
    
    chunks = []
    current_heading = None

    for page in result.pages:
        for line in page.lines:
            text = line.content
            if is_heading(text):  # Detect headings (custom logic)
                current_heading = text
                chunks.append({"heading": text, "body": "", "page_number": page.page_number})
            elif current_heading:
                chunks[-1]["body"] += " " + text  # Add text to the last chunk

    return chunks

def is_heading(text):
    # Simple logic to detect headings (customize as needed)
    return text.strip().endswith(":") or text.strip().isdigit() or text.lower().startswith("section")

def insert_chunks_to_db(chunks, db_config):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    
    for chunk in chunks:
        cursor.execute("""
            INSERT INTO sow_chunks (document_id, heading, body, level, page_number)
            VALUES (%s, %s, %s, %s, %s)
        """, ("doc_001", chunk['heading'], chunk['body'], 1, chunk['page_number']))
    
    conn.commit()
    cursor.close()
    conn.close()

# Analyze document and store chunks
file_path = "path_to_your_sow_document.pdf"
chunks = analyze_document(file_path)
insert_chunks_to_db(chunks, db_config)

print("Document chunks have been stored in the database.")
