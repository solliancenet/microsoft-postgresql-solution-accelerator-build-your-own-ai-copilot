# ##############################################################################
# Set Azure CLI Context
# ##############################################################################
az account set --subscription "${env:AZURE_SUBSCRIPTION_ID}"

# ##############################################################################
# Install Required Azure CLI Extensions
# ##############################################################################
az config set extension.use_dynamic_install=yes_without_prompt
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
          --file-path "./scripts/sql/deploy-database-tables.sql"

Write-Host "Database Schema Configured"

# ##############################################################################
# Grant Database Permissions to API Identity
# ##############################################################################
Write-Host "Granting Database Permissions to API App Managed Identity..."
# Load script
$sqlScript = Get-Content -Path "./scripts/sql/grant-table-permissions.sql" -Raw
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
# Upload Sample Files to Blob Storage
# ##############################################################################

Write-Host "Uploading Sample Files to Blob Storage..."

az storage blob upload `
    --auth-mode login `
    --overwrite true `
    --account-name "${env:AZURE_STORAGE_ACCOUNT_NAME}" `
    --container-name "${env:AZURE_STORAGE_CONTAINER_NAME}" `
    --name "1/sow/Statement_of_Work_TailWind_Cloud_Solutions_Woodgrove_Bank_20241101.pdf" `
    --file "./data/sample_docs/model_training/Statement_of_Work_TailWind_Cloud_Solutions_Woodgrove_Bank_20241101.pdf"

# az storage blob upload `
#     --auth-mode login `
#     --overwrite true `
#     --account-name "${env:AZURE_STORAGE_ACCOUNT_NAME}" `
#     --container-name "${env:AZURE_STORAGE_CONTAINER_NAME}" `
#     --name "2/sow/Statement_of_Work_Contoso_DevOps_Services_Woodgrove_Bank_20240601.pdf" `
#     --file "./data/sample_docs/model_training/Statement_of_Work_Contoso_DevOps_Services_Woodgrove_Bank_20240601.pdf"

# az storage blob upload `
#     --auth-mode login `
#     --overwrite true `
#     --account-name "${env:AZURE_STORAGE_ACCOUNT_NAME}" `
#     --container-name "${env:AZURE_STORAGE_CONTAINER_NAME}" `
#     --name "3/sow/Statement_of_Work_Lucerne_Publishing_Woodgrove_Bank_20241201.pdf" `
#     --file "./data/sample_docs/model_training/Statement_of_Work_Lucerne_Publishing_Woodgrove_Bank_20241201.pdf"

# az storage blob upload `
#     --auth-mode login `
#     --overwrite true `
#     --account-name "${env:AZURE_STORAGE_ACCOUNT_NAME}" `
#     --container-name "${env:AZURE_STORAGE_CONTAINER_NAME}" `
#     --name "4/sow/Statement_of_Work_Wide_World_Engineering_Woodgrove_Bank_20241001.pdf" `
#     --file "./data/sample_docs/model_training/Statement_of_Work_Wide_World_Engineering_Woodgrove_Bank_20241001.pdf"

# az storage blob upload `
#     --auth-mode login `
#     --overwrite true `
#     --account-name "${env:AZURE_STORAGE_ACCOUNT_NAME}" `
#     --container-name "${env:AZURE_STORAGE_CONTAINER_NAME}" `
#     --name "5/sow/Statement_of_Work_Trey_Research_Inc_Woodgrove_Bank_20240501.pdf" `
#     --file "./data/sample_docs/model_training/Statement_of_Work_Trey_Research_Inc_Woodgrove_Bank_20240501.pdf"

Write-Host "Sample Files Uploaded to Blob Storage"

# # ##############################################################################
# # Create Event Grid Subscription with BlobCreated & BlobUpdated Webhook
# # - this must be created after the app is deployed, otherwise the webhook validation will fail
# # ##############################################################################
Write-Host "Creating Event Grid 'StorageBlob' Subscription with BlobCreated & BlobUpdated Webhook..."

$eventGridStorageBlobSubscriptionExists = az eventgrid system-topic event-subscription list `
    --resource-group "${env:AZURE_RESOURCE_GROUP}" `
    --system-topic-name "${env:STORAGE_EVENTGRID_SYSTEM_TOPIC_NAME}" `
    --query "[?name=='StorageBlob']" `
    --output tsv

if (-not $eventGridStorageBlobSubscriptionExists) {
    az eventgrid system-topic event-subscription create `
        --name "StorageBlob" `
        --system-topic-name "${env:STORAGE_EVENTGRID_SYSTEM_TOPIC_NAME}" `
        --endpoint "${env:SERVICE_API_ENDPOINT_URL}/webhooks/storage-blob" `
        --included-event-types "Microsoft.Storage.BlobCreated" "Microsoft.Storage.BlobUpdated" `
        --subject-begins-with "/blobServices/default/containers/${env:AZURE_STORAGE_CONTAINER_NAME}/blobs/" `
        --resource-group "${env:AZURE_RESOURCE_GROUP}"
}

Write-Host "Event Grid Subscription 'StorageBlob' Created"


# ##############################################################################
# Deploy Machine Learning Model to Azure ML Workspace
# ##############################################################################
# only deploy if ${env:DEPLOY_AML_MODEL} is set to true

$modelDeploymentsJson = az ml online-deployment list `
            --endpoint-name "$env:AZURE_AML_ENDPOINT_NAME" `
            --workspace-name "$env:AZURE_AML_WORKSPACE_NAME" `
            --resource-group "$env:AZURE_RESOURCE_GROUP" `
            --query "[].name" `
            --output tsv
$modelDeployments = $modelDeploymentsJson | ConvertFrom-Json
if ($env:DEPLOY_AML_MODEL -eq $False) {
    Write-Host "Skipping Machine Learning Model Deployment"
} elseif ($modelDeployments -contains "bgev2m3-v1") {
    Write-Host "Machine Learning Model Already Deployed"
} else {
    Write-Host "Deploying Machine Learning Model to Azure ML Workspace..."

    ./scripts/aml/deploy_model.ps1 -ErrorAction Stop
   
    if ($? -eq $False) {
        Write-Error "An error occurred while executing deploy_model.ps1"
    } else {
        Write-Host "Machine Learning Model Deployed"
    }
}

