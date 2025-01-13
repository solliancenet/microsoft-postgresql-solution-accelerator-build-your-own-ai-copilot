from app.lifespan_manager import get_db_connection_pool, get_blob_service_client
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
        Depends(get_blob_service_client)
    ],
    responses = {404: {"description": "Not found"}}
)

@router.post('/storage-blob')
async def storage_blob_webhook(
    request: Request,
    pool = Depends(get_db_connection_pool),
    blob_service_client = Depends(get_blob_service_client)
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

        if (eventType == 'Microsoft.Storage.BlobCreated'):
            print(f"BlobCreated - Container: {containerName} - Filename: {blobName}")
        if (eventType == 'Microsoft.Storage.BlobUpdated'):
            print(f"BlobUpdated - Container: {containerName} - Filename: {blobName}")

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