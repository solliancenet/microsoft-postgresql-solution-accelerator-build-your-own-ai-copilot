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

@description('The Principal ID of user to grant Data Contributor/Reader permissions to the storage account.')
param principalId string

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

resource amlEndpoint 'Microsoft.MachineLearningServices/workspaces/onlineEndpoints@2024-07-01-preview' = {
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

resource storageBlobDataContributorRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: guid(subscription().id, resourceGroup().id, principalId, 'mlStorageBlobDataContributorRole')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe') // Storage Blob Data Contributor role
    principalId: principalId
    principalType: 'User'
  }
}

resource storageBlobDataReaderRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: guid(subscription().id, resourceGroup().id, principalId, 'mlStorageBlobDataContributorRole')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1') // Storage Blob Data Reader role
    principalId: principalId
    principalType: 'User'
  }
}

output AML_WORKSPACE_NAME string = amlWorkspace.name
output AML_ENDPOINT_NAME string = amlEndpoint.name
output AML_ENDPOINT_SCORING_URI string = amlEndpoint.properties.scoringUri
