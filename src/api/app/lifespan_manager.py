from app.services import AzureOpenAIService, DatabaseService, AzureDocIntelligenceService, StorageService, ConfigService
from azure.identity.aio import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from contextlib import asynccontextmanager

# Create a global async Azure OpenAI
aoai_service = None
# Create a global async Microsoft Entra ID RBAC credential
credential = None
# Create a global async PostgreSQL db connection
db = None
# Create a global async AppConfig
config_service = None
# Create a global async StorageService
storage_service = None
# Create a global async Azure Document Intelligence Service client
doc_intelligence_service = None

@asynccontextmanager
async def lifespan(app):
    """Async context manager for the FastAPI application lifespan."""
    global aoai_service
    global config_service
    global credential
    global db
    global doc_intelligence_service
    global storage_service
    
    # Create an async Microsoft Entra ID RBAC credential
    credential = DefaultAzureCredential()

    # Create ConfigService instance
    config_service = ConfigService(credential)

    # Create an async Azure OpenAI chat and embeddings clients
    aoai_service = AzureOpenAIService(credential, await config_service.get_openai_endpoint())

    # Create an async Azure Document Intelligence Service client
    doc_intelligence_credential = AzureKeyCredential(await config_service.get_doc_intelligence_key())
    doc_intelligence_service = AzureDocIntelligenceService(doc_intelligence_credential, await config_service.get_doc_intelligence_endpoint())

    # Create an async Azure Blob Service client
    storage_service = StorageService(credential, await config_service.get_storage_account(), config_service.get_document_container_name())

    # Create a connection to the Azure Database for PostgreSQL server
    db = DatabaseService(credential, await config_service.get_postgresql_server_name(), await config_service.get_postgresql_database_name())

    yield

    # Close the database connection
    await db.close()

    # Close the ConfigService
    await config_service.close()

    # Close the async Microsoft Entra ID RBAC credential
    await credential.close()

# Provide methods for retrieving the global async objects from the lifespan manager.
async def get_config_service():
    return config_service

async def get_credential():
    return credential

async def get_chat_client():
     return await aoai_service.get_chat_client()

async def get_azure_doc_intelligence_service():
    return doc_intelligence_service

async def get_embedding_client():
    return await aoai_service.get_embedding_client()

async def get_storage_service():
    return storage_service

async def get_db_connection_pool():
    return await db.get_connection_pool()
