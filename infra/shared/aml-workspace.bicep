@description('The location of the PostgreSQL server.')
param location string = resourceGroup().location

@description('Workspace name.')
param workspaceName string

@description('Endpoint name.')
param endpointName string

@description('The name of the key vault to use.')
param keyVaultName string

@description('Unique name for the Application Insights instance.')
param appInsightsName string

@description('Unique name for the Storage Account instance.')
param storageAccountName string

@description('Unique name for the Container Registry instance.')
param containerRegistryName string

resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' existing = {
  name: keyVaultName
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: appInsightsName
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' existing = {
  name: storageAccountName
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2022-12-01' existing = {
  name: containerRegistryName
}

resource amlWorkspace 'Microsoft.MachineLearningServices/workspaces@2024-10-01-preview' = {
  name: workspaceName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: workspaceName
    description: 'Azure Machine Learning workspace for integration with PostgreSQL'
    keyVault: keyVault.id
    applicationInsights: appInsights.id
    storageAccount: storageAccount.id
    containerRegistry: containerRegistry.id
    systemDatastoresAuthMode: 'Identity'
  }
}

resource amlOnlineEndpoint 'Microsoft.MachineLearningServices/workspaces/onlineEndpoints@2024-07-01-preview' = {
  name: endpointName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  parent: amlWorkspace
  properties: {
    authMode: 'Key'
    description: 'bge-v2-m3 reranker model endpoint'
  }
}

output AML_WORKSPACE_NAME string = amlWorkspace.name
output AML_ENDPOINT_NAME string = amlOnlineEndpoint.name
output AML_ENDPOINT_SCORING_URI string = amlOnlineEndpoint.properties.scoringUri
