from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

# Usage example:
# key_vault_provider = KeyVaultConfigProvider(os.getenv("AZURE_KEY_VAULT_NAME"))
# secret_value = key_vault_provider.get_secret("my-secret")
# postgresql_server_name = key_vault_provider.get_postgresql_server_name()

class KeyVaultConfigProvider:
    def __init__(self, key_vault_name: str = None):
        self.key_vault_name = key_vault_name
        if self.key_vault_name is None:
            self.key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
        
        self.key_vault_uri = f"https://{self.key_vault_name}.vault.azure.net"

        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.key_vault_uri, credential=self.credential)

        self.cache = {}

    def get_key_vault_name(self) -> str:
        return self.key_vault_name

    def get_secret(self, secret_name: str) -> str:
        if secret_name in self.cache:
            return self.cache[secret_name]
        secret = self.client.get_secret(secret_name).value
        self.cache[secret_name] = secret
        return secret

    def get_postgresql_server_name(self) -> str:
        return self.get_secret("postgresql-server")

    def get_storage_connection_string(self) -> str:
        return self.get_secret("storage-connection")

    def get_document_container_name(self) -> str:
        return "documents"

