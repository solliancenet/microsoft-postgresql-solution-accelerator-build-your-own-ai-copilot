$ServiceName = "web"
$EnvVarName = "SERVICE_USERPORTAL_ENDPOINT_URL"

az account set --subscription $env:AZURE_SUBSCRIPTION_ID

# Ensure kubectl is configured to use the AKS cluster
# Write-Host "Configuring kubectl to use the AKS cluster..."
# az aks get-credentials --resource-group $env:AZURE_RESOURCE_GROUP --name $env:AZURE_AKS_CLUSTER_NAME --overwrite-existing

# Get the external IP of the service
Write-Host "Retrieving the external IP of the $ServiceName service..."
$apiService = kubectl get service $ServiceName -o json | ConvertFrom-Json
$apiIp = $apiService.status.loadBalancer.ingress[0].ip

if (-not $apiIp) {
    Write-Error "Failed to retrieve the IP address for the $ServiceName service."
    exit 1
}

Write-Host "$ServiceName service IP: $apiIp"

# ############################################################
# Persist the service IP as an environment variable with AZD

# Get the azd environment name
$envVarValue = "http://$apiIp"

# Path to the .env file for the current azd environment
$envFilePath = "../../infra/aks/.azure/$env:AZURE_ENV_NAME/.env"

# Check if the .env file exists
if (-Not (Test-Path $envFilePath)) {
    Write-Error "The .env file for the azd environment '$env:AZURE_ENV_NAME' does not exist at path '$envFilePath'."
    exit 1
}

# Check if the environment variable already exists in the .env file
$envFileContent = Get-Content $envFilePath
$envVarPattern = "^$EnvVarName=`"[^`"]*`""

if ($envFileContent -match $envVarPattern) {
    # Update the existing variable
    $updatedContent = $envFileContent -replace $envVarPattern, "$EnvVarName=`"$envVarValue`""
} else {
    # Append the variable to the file
    $updatedContent = $envFileContent + "`n$EnvVarName=`"$envVarValue`""
}

# Write the updated content back to the .env file
Set-Content -Path $envFilePath -Value $updatedContent -Force

Write-Host "Environment variable '$EnvVarName' has been set to '$envVarValue' in the azd environment '$env:AZURE_ENV_NAME'."
