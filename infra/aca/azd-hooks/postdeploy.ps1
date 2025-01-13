# ##############################################################################
# Set Azure CLI Context
# ##############################################################################
az account set --subscription ${env:AZURE_SUBSCRIPTION_ID}

# ##############################################################################
# Install Required Azure CLI Extensions
# ##############################################################################
az extension add -y -n "rdbms-connect"

# ##############################################################################
# Get the current user's name and access token to connect to the PostgreSQL Server
# ##############################################################################
$username=(az account show -o tsv --query "user.name")
$token=(az account get-access-token --resource=https://ossrdbms-aad.database.windows.net -o tsv --query "accessToken")
Write-Host "Access Token Retrieved for $username"

# ##############################################################################
# Add local Public IP Address to PostgreSQL Firewall,
# so we can connect to the PostgreSQL Server and run scripts
# ##############################################################################
$publicIpAddress =  (Invoke-RestMethod -Uri "http://ipinfo.io/ip")
az postgres flexible-server firewall-rule create `
    --resource-group "${env:AZURE_RESOURCE_GROUP}" `
    --name "${env:POSTGRESQL_SERVER_NAME}" `
    --rule-name "AllowAZDLocalMachine" `
    --start-ip-address $publicIpAddress `
    --end-ip-address $publicIpAddress

Write-Host "Added Firewall Rule for $publicIpAddress"

# ##############################################################################
# Add account running AZD as Administrator on PostgreSQL Server,
# so we have necessary permissions to run the database scripts below
# ##############################################################################
az postgres flexible-server ad-admin create `
    --resource-group "${env:AZURE_RESOURCE_GROUP}" `
    --server-name "${env:POSTGRESQL_SERVER_NAME}" `
    --display-name "$username" `
    --object-id "$(az ad user show --id $username --query id -o tsv)"

Write-Host "Added $username as an Admin on PostgreSQL Server"

# ##############################################################################
# Create Database Schema
# ##############################################################################
Write-Host "Configuring Database Schema..."

az postgres flexible-server execute `
          --admin-user "$username" `
          --admin-password "$token" `
          --name "${env:POSTGRESQL_SERVER_NAME}" `
          --database-name "${env:POSTGRESQL_DATABASE_NAME}" `
          --file-path "./scripts/deploy-database-tables.sql"

Write-Host "Database Schema Configured"

# ##############################################################################
# Grant Database Permissions to API Identity
# ##############################################################################
Write-Host "Granting Database Permissions to API App Managed Identity..."
# Load script
$sqlScript = Get-Content -Path "./scripts/grant-table-permissions.sql" -Raw
# Replace environment variable placeholders
$sqlScript = $sqlScript.Replace('${env:SERVICE_API_IDENTITY_PRINCIPAL_NAME}', "${env:SERVICE_API_IDENTITY_PRINCIPAL_NAME}")
# Run script
az postgres flexible-server execute `
          --admin-user "$username" `
          --admin-password "$token" `
          --name "${env:POSTGRESQL_SERVER_NAME}" `
          --database-name "${env:POSTGRESQL_DATABASE_NAME}" `
          --querytext $sqlScript

Write-Host "Database Permissions Granted to API App Managed Identity"

# ##############################################################################
# Configure PostgreSQL Server Extensions with OpenAI and Vector Extensions
# ##############################################################################
Write-Host "Configuring PostgreSQL Server Extensions for OpenAI and Vector..."
# Load script
$sqlScript = Get-Content -Path "./scripts/setup_azure_ai.sql" -Raw
# Replace environment variable placeholders
$sqlScript = $sqlScript.Replace('${env:AZURE_OPENAI_ENDPOINT}', "${env:AZURE_OPENAI_ENDPOINT}").Replace('${env:AZURE_OPENAI_KEY}', "${env:AZURE_OPENAI_KEY}")
# Run script
az postgres flexible-server execute `
          --admin-user "$username" `
          --admin-password "$token" `
          --name "${env:POSTGRESQL_SERVER_NAME}" `
          --database-name "${env:POSTGRESQL_DATABASE_NAME}" `
          --querytext $sqlScript

Write-Host "PostgreSQL Server Extensions Configured"
