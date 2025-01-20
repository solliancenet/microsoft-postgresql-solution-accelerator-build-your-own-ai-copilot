from app.services import AzureOpenAIService, DatabaseService, StorageService, ConfigService
from azure.identity.aio import DefaultAzureCredential
from contextlib import asynccontextmanager

# Create an Azure OpenAI embeddings client
embedding_client = None
# Create an Azure OpenAI chat client
chat_client = None
# Create a global async Microsoft Entra ID RBAC credential
credential = None
# Create a global async PostgreSQL connection pool
db = None
db_connection_pool = None
# Create a global async AppConfig
appConfig = None
# Create a global async StorageService
storage_service = None

@asynccontextmanager
async def lifespan(app):
    """Async context manager for the FastAPI application lifespan."""
    global appConfig
    global chat_client
    global credential
    global db
    global embedding_client
    global storage_service
    
    # Create an async Microsoft Entra ID RBAC credential
    credential = DefaultAzureCredential()

    # Create ConfigService instance
    appConfig = ConfigService(credential)

    # Create an async Azure OpenAI chat and embeddings clients
    aoai_service = AzureOpenAIService(credential, await appConfig.get_openai_endpoint())
    chat_client = await aoai_service.get_chat_client()
    embedding_client = await aoai_service.get_embedding_client()

    # Create an async Azure Blob Service client
    storage_service = StorageService(credential, await appConfig.get_storage_account(), appConfig.get_document_container_name())

    # Create a connection to the Azure Database for PostgreSQL server
    db = DatabaseService(credential, await appConfig.get_postgresql_server_name(), await appConfig.get_postgresql_database_name())
    
    yield

    # Close the async PostgreSQL connection pool
    await db_connection_pool.close()
    # Close the async Microsoft Entra ID RBAC credential
    await credential.close()

# Provide methods for retrieving the global async objects from the lifespan manager.
async def get_app_config():
    return appConfig

async def get_credential():
    return credential

async def get_chat_client():
    return chat_client

async def get_embedding_client():
    return embedding_client

async def get_storage_service():
    return storage_service

async def get_db_connection_pool():
    global db
    return await db.get_connection_pool()
