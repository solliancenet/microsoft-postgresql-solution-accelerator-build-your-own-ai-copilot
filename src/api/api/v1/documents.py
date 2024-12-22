from fastapi import APIRouter, HTTPException, UploadFile, File
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from config import KeyVaultConfigProvider
import os
import uuid
from typing import List

router = APIRouter()

# Initialize Key Vault Config Provider
config_provider = KeyVaultConfigProvider()

# Initialize Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(config_provider.get_storage_connection_string())
container_name = config_provider.get_document_container_name()

# Create container if it doesn't exist
container_client = blob_service_client.get_container_client(container_name)
if not container_client.exists():
    container_client.create_container()
    print(f"Container {container_name} created.")
else:
    print(f"Container {container_name} already exists.")



@router.get("/documents", response_model=List[dict])
def list_documents():
    """
    List all documents in the container, sorted alphabetically by filename.
    """
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs()
        documents = []
        for blob in blob_list:
            blob_client = container_client.get_blob_client(blob)
            blob_properties = blob_client.get_blob_properties()
            metadata = blob_properties.metadata
            documents.append({
                "blob_name": blob.name,
                "filename": metadata.get("filename", "N/A"),
                "created": blob_properties.creation_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            })
        # Sort documents by filename
        documents.sort(key=lambda x: (x["filename"], x["created"]))
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_name}")
def read_document(document_name: str):
    """
    Read a document from the container.
    """
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=document_name)
        download_stream = blob_client.download_blob()
        return download_stream.readall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents")
def write_document(file: UploadFile = File(...)):
    """
    Write a document to the container.
    """
    try:
        # generate guid for blog name
        blobName = str(uuid.uuid4())

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blobName)

        metadata = {"filename": file.filename}
        blob_client.upload_blob(file.file, overwrite=True, metadata=metadata)
        
        return {"message": f"Document {file.filename} uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))