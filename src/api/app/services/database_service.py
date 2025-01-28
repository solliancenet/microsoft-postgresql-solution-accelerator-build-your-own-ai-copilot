import asyncpg
import urllib.parse
from azure.identity.aio import DefaultAzureCredential
from datetime import datetime, timedelta
import asyncio
import jwt
import os

class DatabaseService:
    """Class to manage the connection to the Azure Database for PostgreSQL server."""
    def __init__(self, credential: DefaultAzureCredential, host_name: str, database_name: str):
        self.credential = credential
        self.host_name = host_name
        self.database_name = database_name
        self.connection_pool = None
        self.connection_pool_created = datetime.now()
        self._lock = asyncio.Lock()

    async def close(self):
        """Close the connection pool."""
        if self.connection_pool is None or self.connection_pool._closed:
            return
        await self.connection_pool.close()

    async def get_connection_pool(self):
        """Get the connection pool to the Azure Database for PostgreSQL server."""
        # Create a new connection pool, if it does not exist, is closed, or has been open for more than 45 minutes (Azure token expires after 1 hour)
        sessionExpired = (datetime.now() - self.connection_pool_created) >= timedelta(minutes=45)
        
        if sessionExpired or self.connection_pool is None or self.connection_pool._closed:
            async with self._lock:
                if (sessionExpired):
                    if (self.connection_pool is not None and not self.connection_pool._closed):
                        await self.connection_pool.close()

                connection_uri = await self.__get_connection_uri()
                self.connection_pool = await asyncpg.create_pool(dsn=connection_uri, min_size=1, max_size=150)
                self.connection_pool_created = datetime.now()

        return self.connection_pool
    
    async def __get_azure_entra_token(self):
        token = await self.credential.get_token("https://ossrdbms-aad.database.windows.net/.default")
        return token.token

    async def __get_username(self, token):
        """get username from token or Entra if token does not have username"""
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        # When running as a User, 'upn' will be populated
        # When running as an App, in Azure with Managed Identity, 'AZURE_IDENTITY_NAME" environment variable must be used
        username = decoded_token.get("upn") or os.getenv('AZURE_IDENTITY_NAME')
        return username

    async def __get_connection_uri(self):
        """Get the connection URI for the Azure Database for PostgreSQL server."""
        sslmode = "require"

        # Call get_token() to get a token from Microsft Entra ID and add it as the password in the URI.
        token = await self.__get_azure_entra_token()
        
        # get username for token
        username = await self.__get_username(token)

        # set password to the token
        password = token

        db_uri = f"postgresql://{urllib.parse.quote_plus(username)}:{password}@{self.host_name}:5432/{self.database_name}?sslmode={sslmode}"

        return db_uri
