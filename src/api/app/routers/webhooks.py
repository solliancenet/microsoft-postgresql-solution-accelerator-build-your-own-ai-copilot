from app.lifespan_manager import get_config_service
from fastapi import APIRouter, Depends, Request

# Initialize the router
router = APIRouter(
    prefix = "/webhooks",
    tags = ["Webhooks"],
    dependencies = [
        Depends(get_config_service)
    ],
    responses = {404: {"description": "Not found"}}
)

@router.post('/storage-blob')
async def storage_blob_webhook(
    request: Request,
    app_config = Depends(get_config_service)
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

        # Parse out the blob file name
        blobName = subject.replace(blobNamePrefix, '', 1)

        print(f"Event: {eventType} - Filename: {blobName}")

    return {"message": "Webhook received."}
