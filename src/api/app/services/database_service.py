import asyncpg
import urllib.parse
from azure.identity.aio import DefaultAzureCredential

class DatabaseService:
    """Class to manage the connection to the Azure Database for PostgreSQL server."""
    def __init__(self, credential: DefaultAzureCredential):
        self.credential = credential

    async def get_connection_pool(self):
        connection_uri = await self.__get_connection_uri()
        return await asyncpg.create_pool(dsn=connection_uri)
    
    async def __get_connection_uri(self):
        """Get the connection URI for the Azure Database for PostgreSQL server."""
        # TODO: Get database connection parameters from app configuration.
        # Read URI parameters from the environment
        dbhost = "psql-datauemjxng3p6up6" #os.environ['DBHOST']
        dbname = "db-claimsdata" #os.environ['DBNAME']
        dbuser = "kyle@solliance.net" #urllib.parse.quote(os.environ['DBUSER'])
        sslmode = "require"

        # Call get_token() to get a token from Microsft Entra ID and add it as the password in the URI.
        token = await self.credential.get_token("https://ossrdbms-aad.database.windows.net/.default")
        password = urllib.parse.quote_plus(token.token)

        db_uri = f"postgresql://{urllib.parse.quote_plus(dbuser)}:{password}@{dbhost}.postgres.database.azure.com:5432/{dbname}?sslmode={sslmode}"
        return db_uri