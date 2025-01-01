import asyncpg
import urllib.parse
from azure.identity.aio import DefaultAzureCredential
import jwt
import aiohttp

class DatabaseService:
    """Class to manage the connection to the Azure Database for PostgreSQL server."""
    def __init__(self, credential: DefaultAzureCredential, host_name: str, database_name: str):
        self.credential = credential
        self.host_name = host_name
        self.database_name = database_name

    async def get_connection_pool(self):
        connection_uri = await self.__get_connection_uri()
        return await asyncpg.create_pool(dsn=connection_uri)
    
    async def __get_azure_entra_token(self):
        token = await self.credential.get_token("https://ossrdbms-aad.database.windows.net/.default")
        return token.token

    async def __get_username(self, token):
        """get username from token or Entra if token does not have username"""
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        username = decoded_token.get("preferred_username") or decoded_token.get("upn")
        # if username is None
        if username is None:
            # call Entra to get userPrincipalName
            username = await self.__get_authenticated_entity_name()
        return username

    async def __get_authenticated_entity_name(self) -> str:
        """Get the name of the authenticated entity."""
        try:
            # Get an access token for Microsoft Graph
            token = await self.credential.get_token("https://graph.microsoft.com/.default")
            headers = {
                "Authorization": f"Bearer {token.token}"
            }
            
            # Call the Microsoft Graph /me endpoint
            async with aiohttp.ClientSession() as session:
                async with session.get("https://graph.microsoft.com/v1.0/me", headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        # Return user or service principal name
                        return result.get("userPrincipalName") or result.get("displayName")
                    else:
                        error = await response.text()
                        raise Exception(f"Error fetching entity: {error}")
        except Exception as e:
            return f"Failed to retrieve entity name: {str(e)}"


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