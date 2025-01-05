from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient
import os

# Usage example:
# appConfig = AppConfig(os.getenv("AZURE_KEY_VAULT_NAME"))
# secret_value = appConfig.get_secret("my-secret")
# postgresql_server_name = appConfig.get_postgresql_server_name()

class ConfigService:
    def __init__(self, credential: DefaultAzureCredential, key_vault_name: str = None):
        self.credential = credential

        self.key_vault_name = key_vault_name
        if self.key_vault_name is None:
            self.key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
        
        self.key_vault_uri = f"https://{self.key_vault_name}.vault.azure.net"

        self.client = SecretClient(vault_url=self.key_vault_uri, credential=self.credential)

    async def get_key_vault_name(self) -> str:
        return await self.key_vault_name

    async def __get_secret(self, secret_name: str) -> str:
        secret = await self.client.get_secret(secret_name)
        return secret.value

    async def get_openai_service(self) -> str:
        return await self.__get_secret("openai-service")

    async def get_postgresql_server_name(self) -> str:
        return await self.__get_secret("postgresql-server")
    
    async def get_postgresql_database_name(self) -> str:
        return await self.__get_secret("postgresql-database")

    async def get_storage_account(self) -> str:
        return await self.__get_secret("storage-account")

    def get_document_container_name(self) -> str:
        return "documents"

