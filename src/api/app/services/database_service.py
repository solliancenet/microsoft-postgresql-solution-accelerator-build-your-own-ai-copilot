import asyncpg
import urllib.parse
from azure.identity.aio import DefaultAzureCredential
import jwt

class DatabaseService:
    """Class to manage the connection to the Azure Database for PostgreSQL server."""
    def __init__(self, credential: DefaultAzureCredential, host_name: str, database_name: str):
        self.credential = credential
        self.host_name = host_name
        self.database_name = database_name

    async def get_connection_pool(self):
        connection_uri = await self.__get_connection_uri()
        return await asyncpg.create_pool(dsn=connection_uri)
    
    async def __get_connection_uri(self):
        """Get the connection URI for the Azure Database for PostgreSQL server."""
        sslmode = "require"

        # Call get_token() to get a token from Microsft Entra ID and add it as the password in the URI.
        token = await self.credential.get_token("https://ossrdbms-aad.database.windows.net/.default")
        password = urllib.parse.quote_plus(token.token)

        # get username from token
        decoded_token = jwt.decode(token.token, options={"verify_signature": False})
        username = decoded_token.get("preferred_username") or decoded_token.get("upn")

        db_uri = f"postgresql://{urllib.parse.quote_plus(username)}:{password}@{self.host_name}:5432/{self.database_name}?sslmode={sslmode}"
        return db_uri