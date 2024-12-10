#! /usr/bin/pwsh

Param(
    [parameter(Mandatory=$false)][string]$cosmosDbAccountName=$env:AZURE_COSMOS_DB_NAME,
    [parameter(Mandatory=$false)][string]$resourceGroup=$env:AZURE_RESOURCE_GROUP,
    [parameter(Mandatory=$false)][string]$apiUrl=$env:SERVICE_API_ENDPOINT_URL
)

Write-Host "postdeploy hook"

