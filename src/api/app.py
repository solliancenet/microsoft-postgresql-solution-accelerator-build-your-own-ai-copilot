"""
API entrypoint for backend API.
"""
import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

load_dotenv()

app = FastAPI(docs_url="/")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agent pool keyed by session_id to retain memories/history in-memory.
# Note: the context is lost every time the service is restarted.
agent_pool = {}

@app.get("/status")
def root():
    """
    Health probe endpoint.
    """

    key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")

    return {"status": "ready", "keyvault-name": key_vault_name}

    # key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
    # credential = DefaultAzureCredential()
    # client = SecretClient(vault_url=key_vault_uri, credential=credential)
    # postgresql_server_name = client.get_secret("postgresql-server").value 

    # return {"status": "ready", "keyvault-name": key_vault_name, "postgresql-server-name": postgresql_server_name}
