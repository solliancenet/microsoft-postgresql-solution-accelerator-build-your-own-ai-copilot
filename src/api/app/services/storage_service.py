from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import ContentSettings
from fastapi import UploadFile

class StorageService:
    def __init__(self, credential: DefaultAzureCredential, storage_account_name: str, container_name: str):
        self.credential = credential
        self.storage_account_name = storage_account_name
        self.container_name = container_name

    async def __get_blob_service_client(self):
        """
        Retrieves a blob service client.
        """
        account_blob_endpoint = f"https://{self.storage_account_name}.blob.core.windows.net/"
        return BlobServiceClient(account_url=account_blob_endpoint, credential=self.credential)

    async def get_container_client(self, container_name: str):
        """
        Retrieves a container client.
        """
        blob_service_client = await self.__get_blob_service_client()
        return blob_service_client.get_container_client(container_name)

    async def get_blob_client(self, container: str, blob: str):
        """
        Retrieves a blob client.
        """
        blob_service_client = await self.__get_blob_service_client()
        return blob_service_client.get_blob_client(container=container, blob=blob)

    # ###########################################################################################

    async def __save_file(self, blobName: str, file: UploadFile):
        """
        Saves a file to Azure Blob Storage.
        """
        blob_service_client = await self.__get_blob_service_client()
        
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=blobName)

        content_settings = ContentSettings(
                content_type=file.content_type,
                content_disposition=f'attachment; filename="{file.filename}"'
            )

        await blob_client.upload_blob(file.file.read(), overwrite=True, content_settings=content_settings)

        return blobName

    async def __save_vendor_document(self, vendor_id: int, docType: str, file: UploadFile):
        """
        Saves a vendor document to Azure Blob Storage.
        """
        blobName = f"{vendor_id}/{docType}/{file.filename}"
        return await self.__save_file(blobName, file)

    async def save_sow_document(self, vendor_id: int, file: UploadFile):
        """
        Saves a SOW document to Azure Blob Storage.
        """
        return await self.__save_vendor_document(vendor_id, "sows", file)

    async def save_invoice_document(self, file: UploadFile):
        """
        Saves a file to Azure Blob Storage.
        """
        blobName = f"invoices/{file.filename}"

        blob_service_client = await self.__get_blob_service_client()
        
        blob_client = await blob_service_client.get_blob_client(container=self.container_name, blob=blobName)

        content_settings = ContentSettings(
                content_type=file.content_type,
                content_disposition=f'attachment; filename="{file.filename}"'
            )

        await blob_client.upload_blob(file.file.read(), overwrite=True, content_settings=content_settings)

        return blobName

    async def delete_document(self, blobName: str):
        """
        Deletes a document from Azure Blob Storage.
        """
        blob_service_client = await self.__get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=blobName)
        if await blob_client.exists():
            await blob_client.delete_blob()