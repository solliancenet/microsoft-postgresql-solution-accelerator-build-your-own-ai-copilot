from app.lifespan_manager import get_db_connection_pool, get_azure_doc_intelligence_service, get_storage_service, get_app_config, get_embedding_client
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from pydantic import parse_obj_as
import json

# Initialize the router
router = APIRouter(
    prefix = "/webhooks",
    tags = ["Webhooks"],
    dependencies = [
        Depends(get_db_connection_pool),
        Depends(get_storage_service),
        Depends(get_azure_doc_intelligence_service),
        Depends(get_embedding_client)
    ],
    responses = {404: {"description": "Not found"}}
)

@router.post('/storage-blob')
async def storage_blob_webhook(
    request: Request,
    pool = Depends(get_db_connection_pool),
    storage_service = Depends(get_storage_service),
    app_config = Depends(get_app_config),
    doc_intelligence_service = Depends(get_azure_doc_intelligence_service),
    embeddings_client = Depends(get_embedding_client)
):
    """Handles incoming webhooks from Azure Blob Storage."""
    # Validate Event Grid Subscription confirmation
    if request.headers.get('aeg-event-type') == 'SubscriptionValidation':
        event_data = await request.json()
        print(event_data)
        validation_code = event_data[0]['data']['validationCode']
        return {"validationResponse": validation_code}

    # Handle Blob Storage events
    # Parse the request body
    events = await request.json()
    print(events)
    # Process each event
    for event in events:
        eventType = event['eventType']
        containerName = event['data']['container']['name']
        blobName = event['data']['blob']['name']

        print(f"Event: {eventType} - Container: {containerName} - Filename: {blobName}")
        
        # Step 1: Download the document
        document_data = await storage_service.download_blob(blobName)

        # Step 2: Extract text from the document
        extracted_text = doc_intelligence_service.extract_text_from_document(document_data)
        full_text = "\n".join(extracted_text)

        # Step 3: Chunk the text semantically
        text_chunks = semantic_chunking(full_text)

        # Step 4: Generate embeddings for the chunks
        embeddings = embeddings_client.embed_documents(text_chunks)

        # Step 5: Insert into database
        # Get doc type and id
        async with pool.acquire() as conn:
            docs = await conn.fetchrow('''
                (
                    select id as id, 'sow' as doctype from sows where document LIKE CONCAT($1, '%')
                ) UNION (
                    select id as id, 'invoice' as doctype from invoices where document LIKE CONCAT($1, '%')
                ) LIMIT 1;
            ''', blobName)
            if docs is None:
                raise HTTPException(status_code=404, detail=f'Document with the name {blobName} was not found in the database.')
            objectId = docs[0]['id']
            documentType = docs[0]['doctype']

        if (documentType == 'sow'): # Insert into SOWs table
            metadata = {
                "content": full_text
            }
            await conn.execute('''
                UPDATE sows
                SET embeddings = $1, metadata = $2
                WHERE id = $3;
            ''', embeddings, json.dumps(metadata), objectId)

        elif (documentType == 'invoice'): # Insert into Invoices table
            metadata = extract_invoice_metadata(full_text)
            await conn.execute('''
                UPDATE invoices
                SET extracted_text = $2, embeddings = $3, metadata = $4, invoice_date = $5, payment_status = $6, chunk_text = $7
                WHERE id = $8;
            ''', metadata['number'], embeddings, json.dumps(metadata), metadata['invoice_date'], metadata['payment_status'], chunk_text, objectId)

        else:
            raise HTTPException(status_code=500, detail=f'Unknown document type: {documentType}')
    

    return {"message": "Webhook received."}


# [{'id': 'a0ed18dd-6cd2-4ed6-9d2b-8b5b626960fb',
#  'topic': '/subscriptions/8c924580-ce70-48d0-a031-1b21726acc1a/resourceGroups/ms-postgresql-byoc',
#  'subject': '',
#  'data': {
# 'validationCode': 'FF4E993B-3651-476E-9E6C-CCB40370ECB6', 
# 'validationUrl': 'https://rp-global.eventgrid.azure.net:553/eventsubscriptions/evgt-uemjxng3p6up6-storageblob/validate?id=FF4E993B-3651-476E-9E6C-CCB40370ECB6&t=2025-01-13T22:47:49.8560291Z&apiVersion=2022-06-15&token=nNcWhdaHV5eybvUxc05PiY2v2L7C04DDD9KMbJduuDI%3d'
# }, 
# 'eventType': 'Microsoft.EventGrid.SubscriptionValidationEvent',
#  'eventTime': '2025-01-13T22:47:49.856086Z', 
# 'metadataVersion': '1', 
# 'dataVersion': '2'}]

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