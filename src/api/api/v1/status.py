from fastapi import APIRouter, HTTPException
from config import KeyVaultConfigProvider

router = APIRouter()

# Initialize Key Vault Config Provider
config_provider = KeyVaultConfigProvider()

@router.get("/status")
def root():
    """
    Health probe endpoint.
    """
    return {
        "status": "ready",
        "keyvault-name": config_provider.get_key_vault_name(),
        "postgresql-server-name": config_provider.get_postgresql_server_name()
    }

    # key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
    # credential = DefaultAzureCredential()
    # client = SecretClient(vault_url=key_vault_uri, credential=credential)
    # postgresql_server_name = client.get_secret("postgresql-server").value 

    # return {"status": "ready", "keyvault-name": key_vault_name, "postgresql-server-name": postgresql_server_name}
