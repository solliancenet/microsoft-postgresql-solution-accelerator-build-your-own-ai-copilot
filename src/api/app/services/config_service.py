from azure.identity.aio import DefaultAzureCredential
from azure.appconfiguration.aio import AzureAppConfigurationClient
from azure.keyvault.secrets.aio import SecretClient
from azure.core.exceptions import ResourceNotFoundError
import os
import json

# Usage example:
# appConfig = AppConfig(os.getenv("AZURE_KEY_VAULT_NAME"))
# secret_value = appConfig.get_secret("my-secret")
# postgresql_server_name = appConfig.get_postgresql_server_name()

class ConfigService:
    def __init__(self, credential: DefaultAzureCredential, app_config_endpoint: str = None):
        self.credential = credential

        self.app_config_endpoint = app_config_endpoint
        if self.app_config_endpoint is None:
            self.app_config_endpoint = os.getenv("AZURE_APP_CONFIG_ENDPOINT")
        
        self.client = AzureAppConfigurationClient(self.app_config_endpoint, credential=self.credential)

    async def __get_setting(self, key: str) -> str:
        try:
            setting = await self.client.get_configuration_setting(key=key)
            
            value = setting.value

            if setting.content_type == "application/vnd.microsoft.appconfig.keyvaultref+json;charset=utf-8":
                # Load value from Key Vault
                key_vault_reference_json = json.loads(value)
                key_vault_url = key_vault_reference_json["uri"]
                key_vault_client = SecretClient(vault_url=f"https://{key_vault_url.split('/')[2]}", credential=self.credential)
                secret_name = key_vault_url.split('/')[-1]
                secret = await key_vault_client.get_secret(secret_name)
                value = secret.value
                await key_vault_client.close()

            return value
        except ResourceNotFoundError:
            raise Exception(f"Setting '{key}' not found in Azure App Configuration.")

    async def get_openai_endpoint(self) -> str:
        return await self.__get_setting("openai-endpoint")

    async def get_postgresql_server_name(self) -> str:
        return await self.__get_setting("postgresql-server")
    
    async def get_postgresql_database_name(self) -> str:
        return await self.__get_setting("postgresql-database")

    async def get_storage_account(self) -> str:
        return await self.__get_setting("storage-account")

    async def get_doc_intelligence_key(self) -> str:
        return await self.__get_setting("doc-intelligence-key")

    async def get_doc_intelligence_endpoint(self) -> str:
        return await self.__get_setting("doc-intelligence-endpoint")

    def get_document_container_name(self) -> str:
        return "documents"

