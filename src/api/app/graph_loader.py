import os
from agefreighter import Factory
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient

async def main():
    """Load data into Azure Database for PostgreSQL Graph Database."""
    # Load environment variables from the .env file
    load_dotenv()
    print("Loading environment variables...")

    # Get environment variables
    server = os.getenv("POSTGRESQL_SERVER_NAME")
    database = 'contracts'
    username = os.getenv("ENTRA_ID_USERNAME")
    account_name = os.getenv("STORAGE_ACCOUNT_NAME")

    # Create an AGEFreigher factory instance to load data from multiple CSV files.
    print("Creating AGEFreighter factory instance...")
    factory = Factory.create_instance('MultiCSVFreighter')

    # Connect to the PostgreSQL database.
    print("Connecting to the PostgreSQL database...")
    await factory.connect(
        dsn=get_connection_string(server, database, username),
        max_connections=64
    )

    local_data_dir = 'graph_data/'

    # Download CSV data files from Azure Blob Storage
    print("Downloading CSV files from Azure Blob Storage...")
    await download_csvs(account_name, local_data_dir)

    # Load data into the graph database
    print("Loading data into the graph database...")
    await factory.load(
        graph_name='vendor_graph',
        vertex_csv_paths = [
            f'{local_data_dir}vendors.csv',
            f'{local_data_dir}sows.csv',
            f'{local_data_dir}invoice_validation_results.csv'
        ],
        vertex_labels = ['vendor', 'sow', 'invoice_validation_result'],
        edge_csv_paths = [f'{local_data_dir}has_invoices.csv'],
        edge_types = ["has_invoices"],
        use_copy=True,
        drop_graph=True,
        create_graph=True,
        progress=True
    )

    print("Graph data loaded successfully!")

def get_connection_string(server_name: str, database_name: str, username: str):
    """Get the connection string for the PostgreSQL database."""
    
    # Get a token for the Azure Database for PostgreSQL server
    credential = DefaultAzureCredential()
    token = credential.get_token("https://ossrdbms-aad.database.windows.net")
    port = 5432

    conn_str = "host={} port={} dbname={} user={} password={}".format(
        server_name, port, database_name, username, token.token
    )
    return conn_str

async def download_csvs(account_name:str, local_data_directory: str):
    """Download CSV files from Azure Blob Storage."""

    # Create connection to the blob storage account
    account_blob_endpoint = f"https://{account_name}.blob.core.windows.net/"
    # Connect to the blob service client using Entra ID authentication
    client = BlobServiceClient(account_url=account_blob_endpoint, credential=DefaultAzureCredential())

    # List the blobs in the graph container with a CSV extension
    async with client:
        async for blob in client.get_container_client('graph').list_blobs():
            if blob.name.endswith('.csv'):
                # Download the CSV file to a local directory
                await download_csv(client, blob.name, local_data_directory)

async def download_csv(client: BlobServiceClient, blob_path: str, local_data_dir: str):
    """Download a CSV file from Azure Blob Storage."""
    # Get the blob
    blob_client = client.get_blob_client(container='graph', blob=blob_path)

    async with blob_client:
        # Download the CSV file
        if await blob_client.exists():
            # create a local directory if it does not exist
            if not os.path.exists(local_data_dir):
                os.makedirs(local_data_dir)

            with open(f'{local_data_dir}{blob_path.split('/')[-1]}', 'wb') as file:
                stream = await blob_client.download_blob()
                result = await stream.readall()
                # Save the CSV file to a local directory
                file.write(result)

if __name__ == "__main__":
    import asyncio
    import sys

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())