from app.lifespan_manager import get_db_connection_pool, get_azure_doc_intelligence_service, get_storage_service, get_config_service
from fastapi import APIRouter, Depends, HTTPException, Request, Form
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
        Depends(get_azure_doc_intelligence_service)
    ],
    responses = {404: {"description": "Not found"}}
)

@router.post('/storage-blob')
async def storage_blob_webhook(
    request: Request,
    pool = Depends(get_db_connection_pool),
    storage_service = Depends(get_storage_service),
    app_config = Depends(get_config_service),
    doc_intelligence_service = Depends(get_azure_doc_intelligence_service)
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
        subject = event['subject']

        blobContainerName = app_config.get_document_container_name()
        blobNamePrefix = f"/blobServices/default/containers/{blobContainerName}/blobs/"
        
        # Check that event is from "documents" container
        # if (subject.substring(0, blobNamePrefix.length) != blobNamePrefix):
        #     raise HTTPException(status_code=400, detail=f"Event subject is not from the '{blobContainerName}' container. (Subject: {subject})")

        # Parse out the blob file name
        blobName = subject.replace(blobNamePrefix, '', 1)

        print(f"Event: {eventType} - Filename: {blobName}")
        


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

# [{'topic': '/subscriptions/8c924580-ce70-48d0-a031-1b21726acc1a/resourceGroups/ms-postgresql-byoc/providers/Microsoft.Storage/storageAccounts/stuemjxng3p6up6', 
# 'subject': '/blobServices/default/containers/documents/blobs/1/sows/Statement_of_Work_TailWind_Cloud_Solutions_Woodgrove_Bank_20241101.pdf', 
# 'eventType': 'Microsoft.Storage.BlobCreated', 
# 'id': '9dd54c42-601e-003a-593c-6d3d2806c3a1',
#  'data': {
#     'api': 'PutBlob', 
#     'clientRequestId': 'fc68f988-d92f-11ef-a509-e2ca5b809811', 'requestId': '9dd54c42-601e-003a-593c-6d3d28000000', 'eTag': '0x8DD3B53E0AE4303', 
#     'contentType': 'application/pdf', 'contentLength': 3529, 'blobType': 'BlockBlob', 'accessTier': 'Default', 
#     'url': 'https://stuemjxng3p6up6.blob.core.windows.net/documents/1/sows/Statement_of_Work_TailWind_Cloud_Solutions_Woodgrove_Bank_20241101.pdf',
#      'sequencer': '0000000000000000000000000000F124000000000007e0c7', 'storageDiagnostics': {'batchId': '7679938c-f006-0070-003c-6d0d4f000000'}
#      }, 'dataVersion': '', 'metadataVersion': '1', 'eventTime': '2025-01-23T02:15:59.4329615Z'}]
