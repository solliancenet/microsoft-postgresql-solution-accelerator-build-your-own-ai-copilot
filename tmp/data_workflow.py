import os
import json
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
import psycopg2
import re
from datetime import datetime

# Environment Variables
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
FORM_RECOGNIZER_ENDPOINT = os.getenv("FORM_RECOGNIZER_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("FORM_RECOGNIZER_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
POSTGRESQL_CONNECTION = os.getenv("POSTGRESQL_CONNECTION")

# Initialize Clients
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
document_analysis_client = DocumentAnalysisClient(
    endpoint=FORM_RECOGNIZER_ENDPOINT,
    credential=AzureKeyCredential(FORM_RECOGNIZER_KEY)
)
openai.api_key = OPENAI_API_KEY

# PostgreSQL Connection
conn = psycopg2.connect(POSTGRESQL_CONNECTION)
cursor = conn.cursor()

def download_blob(container_name, blob_name):
    """Download a blob from Azure Blob Storage."""
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    return blob_client.download_blob().readall()

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

def extract_invoice_metadata(full_text):
    """Extract invoice metadata such as number, amount, and invoice_date from text."""
    metadata = {}

    # Extract invoice number
    match = re.search(r"Invoice Number[:\s]+([A-Za-z0-9-]+)", full_text, re.IGNORECASE)
    metadata['number'] = match.group(1) if match else "UNKNOWN"

    # Extract invoice amount
    match = re.search(r"Total Amount[:\s]+[$]?([\d,]+(?:\.\d{1,2})?)", full_text, re.IGNORECASE)
    metadata['amount'] = float(match.group(1).replace(",", "")) if match else 0.0

    # Extract invoice date
    match = re.search(r"Invoice Date[:\s]+([\d/-]{8,10})", full_text, re.IGNORECASE)
    if match:
        try:
            metadata['invoice_date'] = datetime.strptime(match.group(1), "%Y-%m-%d").date()
        except ValueError:
            metadata['invoice_date'] = None
    else:
        metadata['invoice_date'] = None

    # Default payment status
    metadata['payment_status'] = "Pending"

    return metadata


def semantic_chunking(text):
    """Chunk text into semantically meaningful pieces."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,         # Maximum characters per chunk
        chunk_overlap=50        # Overlap between chunks
    )
    return text_splitter.split_text(text)

def generate_embeddings(text_chunks):
    """Generate embeddings for each chunk using OpenAI."""
    embeddings = []
    for chunk in text_chunks:
        response = openai.Embedding.create(
            input=chunk,
            model="text-embedding-ada-002"  # Replace with "text-embedding-3-large" if available
        )
        embeddings.append(response['data'][0]['embedding'])
    return embeddings

def insert_into_postgresql(document_id, full_text, text_chunks, embeddings, metadata):
    """Insert extracted metadata, text chunks, and embeddings into PostgreSQL."""
    # Extract metadata from full text
    extracted_metadata = extract_invoice_metadata(full_text)

    # Insert chunks with metadata
    for chunk_id, (chunk_text, embedding) in enumerate(zip(text_chunks, embeddings)):
        cursor.execute("""
            INSERT INTO invoices (
                number, amount, invoice_date, payment_status, document, metadata, chunk_id, chunk_text, embeddings
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id, chunk_id) DO NOTHING;
        """, (
            extracted_metadata['number'],
            extracted_metadata['amount'],
            extracted_metadata['invoice_date'],
            extracted_metadata['payment_status'],
            full_text,
            json.dumps(metadata),
            chunk_id,
            chunk_text,
            embedding
        ))
    conn.commit()

def process_document(container_name, blob_name, document_id):
    """Complete workflow for processing a document."""
    print(f"Processing document {document_id} from container {container_name}...")
    
    # Step 1: Download the PDF
    document_data = download_blob(container_name, blob_name)

    # Step 2: Extract text from the document
    extracted_text = extract_text_from_document(document_data)
    full_text = "\n".join(extracted_text)

    # Step 3: Chunk the text semantically
    text_chunks = semantic_chunking(full_text)

    # Step 4: Generate embeddings for the chunks
    embeddings = generate_embeddings(text_chunks)

    # Step 5: Insert into PostgreSQL
    metadata = {"container_name": container_name, "blob_name": blob_name}
    insert_into_postgresql(document_id, full_text, text_chunks, embeddings, metadata)

    print(f"Completed processing document {document_id}.")


# Example Usage
if __name__ == "__main__":
    container_name = "documents"
    blob_name = "INV-TWC2024-001.pdf"
    document_id = blob_name.replace(".pdf", "")

    process_document(container_name, blob_name, document_id)

    # Close PostgreSQL connection
    cursor.close()
    conn.close()
