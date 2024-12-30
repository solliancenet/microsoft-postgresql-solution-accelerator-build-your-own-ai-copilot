from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from app.lifespan_manager import get_blob_service_client
from azure.core.exceptions import ResourceNotFoundError
import os

router = APIRouter(
    prefix = "/documents",
    tags = ["Documents"],
    dependencies = [Depends(get_blob_service_client)],
)

@router.get("/{container_name}", response_model = list[dict])
async def get(container_name: str, blob_service_client = Depends(get_blob_service_client)):
    """
    Retrieves a list of all documents in the specified blob container.
    Blobs are returned in an alphabetically sorted list by filename.
    """
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blobs = []
        async for blob in container_client.list_blobs():
            blob_properties = await container_client.get_blob_client(blob).get_blob_properties()
            blobs.append({
                "blob_name": blob.name,
                "filename": os.path.basename(blob.name),
                "content_type": blob_properties.content_settings.content_type,
                "created": blob_properties.creation_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "size": blob_properties.size
            })
        # Sort documents by filename
        blobs.sort(key=lambda x: (x["filename"], x["created"]))
        return blobs
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.reason)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{container_name}/{blob_name}")
async def get_document(container_name: str, blob_name: str, blob_service_client = Depends(get_blob_service_client)):
    """
    Reads the specified document from the container.
    """
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_properties = await blob_client.get_blob_properties()
        download_stream = await blob_client.download_blob()
        content = await download_stream.readall()
        headers = {
            "Content-Type": blob_properties.content_settings.content_type,
            "Content-Disposition": f'attachment; filename="{os.path.basename(blob_client.blob_name)}"'
        }
        return Response(content=content, headers=headers)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.reason)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{container_name}")
async def upload_document(container_name: str, file: UploadFile = File(...), blob_service_client = Depends(get_blob_service_client)):
    """
    Upload a document to the specified container.
    """
    try:
        container_client = blob_service_client.get_container_client(container_name)

        # Check if the container exists, if not create it
        if not await container_client.exists():
            await container_client.create_container()

        blob_client = container_client.get_blob_client(blob=file.filename)
        await blob_client.upload_blob(file.file, overwrite=True)
        
        return {"message": f"Document {file.filename} uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{container_name}/{blob_name}")
async def delete_document(container_name: str, blob_name: str, blob_service_client = Depends(get_blob_service_client)):
    """
    Delete a document from the container.
    """
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        await blob_client.delete_blob()
        return {"message": f"Document {blob_name} deleted successfully."}
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.reason)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))