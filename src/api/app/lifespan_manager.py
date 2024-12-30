import asyncpg
import urllib.parse
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from azure.storage.blob.aio import BlobServiceClient
from contextlib import asynccontextmanager
#from openai import AsyncAzureOpenAI
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

# Create an Azure OpenAI embeddings client
azure_openai_embeddings_client = None
# Create an Azure OpenAI chat client
azure_openai_chat_client = None
# Create a global async Azure Blob Service client
blob_service_client = None
# Create a global async Microsoft Entra ID RBAC credential
credential = None
# Create a global async PostgreSQL connection pool
postgres_connection_pool = None

@asynccontextmanager
async def lifespan(app):
    """Async context manager for the FastAPI application lifespan."""
    global azure_openai_embeddings_client
    global azure_openai_chat_client
    global blob_service_client
    global credential
    global postgres_connection_pool

    # Create an async Microsoft Entra ID RBAC credential
    credential = DefaultAzureCredential()

    # Create an async Azure OpenAI embeddings client
    azure_openai_embeddings_client = await __get_azure_openai_client(credential, "embeddings")

    # Create an async Azure OpenAI chat client
    azure_openai_chat_client = await __get_azure_openai_client(credential, "chat")

    # Create an async Azure Blob Service client
    blob_service_client = await __get_blob_service_client(credential)

    # Create a connection to the Azure Database for PostgreSQL server
    db_uri = await __get_connection_uri(credential)
    postgres_connection_pool = await asyncpg.create_pool(dsn=db_uri)
    
    yield

    # Close the async Azure OpenAI client
    await azure_openai_embeddings_client.close()
    # Close the async Azure OpenAI client
    await azure_openai_chat_client.close()
    # Close the async Azure Blob Service client
    await blob_service_client.close()
    # Close the async PostgreSQL connection pool
    await postgres_connection_pool.close()
    # Close the async Microsoft Entra ID RBAC credential
    await credential.close()

async def get_credential():
    return credential

async def get_azure_openai_embeddings_client():
    return azure_openai_embeddings_client

async def get_azure_openai_chat_client():
    return azure_openai_chat_client

async def get_azure_openai_client(client_type: str):
    if client_type == 'embeddings':
        return azure_openai_embeddings_client
    elif client_type == 'chat':
        return azure_openai_chat_client
    else:
        raise ValueError(f"Invalid client type: {client_type}")

async def get_blob_service_client():
    return blob_service_client

async def get_pool():
    return postgres_connection_pool

# IMPORTANT! This code is for demonstration purposes only. It's not suitable for use in production. 
# For example, tokens issued by Microsoft Entra ID have a limited lifetime (24 hours by default). 
# In production code, you need to implement a token refresh policy.

async def __get_connection_uri(credential: DefaultAzureCredential):
    """Get the connection URI for the Azure Database for PostgreSQL server."""
    # TODO: Get database connection parameters from app configuration.
    # Read URI parameters from the environment
    dbhost = "psql-datauemjxng3p6up6" #os.environ['DBHOST']
    dbname = "db-claimsdata" #os.environ['DBNAME']
    dbuser = "kyle@solliance.net" #urllib.parse.quote(os.environ['DBUSER'])
    sslmode = "require"

    # Use passwordless authentication via DefaultAzureCredential.
    # IMPORTANT! This code is for demonstration purposes only. DefaultAzureCredential() is invoked on every call.
    # In practice, it's better to persist the credential across calls and reuse it so you can take advantage of token
    # caching and minimize round trips to the identity provider. To learn more, see:
    # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/TOKEN_CACHING.md 
    #credential = DefaultAzureCredential()

    # Call get_token() to get a token from Microsft Entra ID and add it as the password in the URI.
    # Note the requested scope parameter in the call to get_token, "https://ossrdbms-aad.database.windows.net/.default".
    token = await credential.get_token("https://ossrdbms-aad.database.windows.net/.default")
    password = urllib.parse.quote_plus(token.token)

    db_uri = f"postgresql://{urllib.parse.quote_plus(dbuser)}:{password}@{dbhost}.postgres.database.azure.com:5432/{dbname}?sslmode={sslmode}"
    return db_uri

async def __get_blob_service_client(credential: DefaultAzureCredential):
    """
    Retrieves a blob service client.
    """
    # TODO: Get storage account name from app configuration.
    storage_account_name = "stuemjxng3p6up6"
    account_blob_endpoint = f"https://{storage_account_name}.blob.core.windows.net/"
    return BlobServiceClient(account_url=account_blob_endpoint, credential=credential)

async def __get_azure_openai_client(credential: DefaultAzureCredential, client_type: str):
    """Creates an Azure OpenAI client."""
    # TODO: Get Azure OpenAI configuration from app configuration.
    # Azure OpenAI configuration
    AZURE_OPENAI_ENDPOINT = "https://openai-uemjxng3p6up6.openai.azure.com/" #"<AZURE_OPENAI_ENDPOINT>"
    AZURE_OPENAI_API_VERSION = "2024-10-21"
    COMPLETION_DEPLOYMENT_NAME = "completions"
    EMBEDDING_DEPLOYMENT_NAME = "embeddings"
    
    # Create an Azure OpenAI client
    if client_type == 'embeddings':
        client = AzureOpenAIEmbeddings(
           azure_deployment = EMBEDDING_DEPLOYMENT_NAME,
           azure_endpoint = AZURE_OPENAI_ENDPOINT,
           azure_ad_token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
       )
    elif client_type == 'chat':
        client = AzureChatOpenAI(
            azure_deployment=COMPLETION_DEPLOYMENT_NAME,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_ad_token_provider=get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
        )
    else:
        raise ValueError(f"Invalid client type: {client_type}")

    return client