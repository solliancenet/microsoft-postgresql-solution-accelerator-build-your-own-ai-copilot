from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient

class StorageService:
    def __init__(self, credential: DefaultAzureCredential):
        self.credential = credential

    async def get_blob_service_client(self):
        """
        Retrieves a blob service client.
        """
        # TODO: Get storage account name from app configuration.
        storage_account_name = "stuemjxng3p6up6"
        account_blob_endpoint = f"https://{storage_account_name}.blob.core.windows.net/"
        return BlobServiceClient(account_url=account_blob_endpoint, credential=self.credential)