from app.services import AzureOpenAIService, DatabaseService, StorageService, ConfigService
from azure.identity.aio import DefaultAzureCredential
from contextlib import asynccontextmanager

# Create an Azure OpenAI embeddings client
embedding_client = None
# Create an Azure OpenAI chat client
chat_client = None
# Create a global async Azure Blob Service client
blob_service_client = None
# Create a global async Microsoft Entra ID RBAC credential
credential = None
# Create a global async PostgreSQL connection pool
db = None
db_connection_pool = None

@asynccontextmanager
async def lifespan(app):
    """Async context manager for the FastAPI application lifespan."""
    global app_config
    global blob_service_client
    global chat_client
    global credential
    global db
    global db_connection_pool
    global embedding_client
    
    # Create an async Microsoft Entra ID RBAC credential
    credential = DefaultAzureCredential()

    # Create ConfigService instance
    appConfig = ConfigService(credential)

    # Create an async Azure OpenAI chat and embeddings clients
    aoai_service = AzureOpenAIService(credential)
    chat_client = await aoai_service.get_chat_client()
    embedding_client = await aoai_service.get_embedding_client()

    # Create an async Azure Blob Service client
    storage_service = StorageService(credential, await appConfig.get_storage_account())
    blob_service_client = await storage_service.get_blob_service_client()

    # Create a connection to the Azure Database for PostgreSQL server
    db = DatabaseService(credential, await appConfig.get_postgresql_server_name(), await appConfig.get_postgresql_database_name())
    db_connection_pool = await db.get_connection_pool()
    
    yield

    # Close the async Azure OpenAI client
    await embedding_client.close()
    # Close the async Azure OpenAI client
    await chat_client.close()
    # Close the async Azure Blob Service client
    await blob_service_client.close()
    # Close the async PostgreSQL connection pool
    await db_connection_pool.close()
    # Close the async Microsoft Entra ID RBAC credential
    await credential.close()

# Provide methods for retrieving the global async objects from the lifespan manager.
async def get_app_config():
    return app_config

async def get_credential():
    return credential

async def get_chat_client():
    return chat_client

async def get_embedding_client():
    return embedding_client

async def get_blob_service_client():
    return blob_service_client

async def get_db_connection_pool():
    global db
    global db_connection_pool
    if (db_connection_pool is None or db_connection_pool._closed):
        db_connection_pool = await db.get_connection_pool()
    return db_connection_pool
