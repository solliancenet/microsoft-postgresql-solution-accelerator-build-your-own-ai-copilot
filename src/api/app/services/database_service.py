import asyncpg
import urllib.parse
from azure.identity.aio import DefaultAzureCredential
import time
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
        self.connection_pool_lock = asyncio.Lock()

        self.azure_token_lock = asyncio.Lock()
        self.azure_token = None
        self.azure_token_created = None

    async def close(self):
        """Close the connection pool."""
        if self.connection_pool is None or self.connection_pool._closed:
            return
        await self.connection_pool.close()

    async def get_connection_pool(self):
        """Get the connection pool to the Azure Database for PostgreSQL server."""

        # check if Azure Token has expired yet
        is_token_expired = await self.__is_azure_token_expired()
        # If connection pool is closed or not defined yet, or the Azure Token is expired, then create a new database connection pool
        if self.connection_pool is None or self.connection_pool._closed or is_token_expired:
            # use lock to make sure this is thread safe
            async with self.connection_pool_lock:

                if (is_token_expired and self.connection_pool is not None and not self.connection_pool._closed):
                    # Be sure to close the connection pool before creating an new one
                    await self.close()

                # get database connection string
                connection_uri = await self.__get_connection_uri()

                # create database connection pool
                self.connection_pool = await asyncpg.create_pool(dsn=connection_uri, min_size=1, max_size=150)

        # return the connection pool
        return self.connection_pool
    
    async def __is_azure_token_expired(self):
        """return true/false if the Azure Token has expired yet"""
        if self.azure_token is None or self.azure_token_created is None:
            return True
        # check if Entra Token has expired
        return self.azure_token.expires_on < time.time()
                
    async def __get_azure_entra_token(self):
        """Get the Azure Token generated to be used for authentication to the database"""
        if self.azure_token is None or self.azure_token_created is None or await self.__is_azure_token_expired():
            async with self.azure_token_lock:
                self.azure_token = await self.credential.get_token("https://ossrdbms-aad.database.windows.net/.default")
        return self.azure_token

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
        # This token will be used as the password in the connection string
        token = (await self.__get_azure_entra_token()).token
        password = token

        # get username for token that will be used in the connection string
        username = await self.__get_username(token)

        # create the full connection string
        db_uri = f"postgresql://{urllib.parse.quote_plus(username)}:{password}@{self.host_name}:5432/{self.database_name}?sslmode={sslmode}"

        return db_uri
