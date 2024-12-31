from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient

class StorageService:
    def __init__(self, credential: DefaultAzureCredential, storage_account_name: str):
        self.credential = credential
        self.storage_account_name = storage_account_name

    async def get_blob_service_client(self):
        """
        Retrieves a blob service client.
        """
        account_blob_endpoint = f"https://{self.storage_account_name}.blob.core.windows.net/"
        return BlobServiceClient(account_url=account_blob_endpoint, credential=self.credential)