@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

param resourceGroupName string

@description('Id of the user or app to assign application roles')
param principalId string

@description('Name of the PostgreSQL database')
param postgresqlDatabaseName string = 'db-claimsdata'

@description('Administrator Login of the PostgreSQL server')
param postgresqlAdminLogin string = 'adminUser'

@description('Administrator Password for the PostgreSQL server')
@secure()
param postgresqlAdminPassword string


param userPortalExists bool
@secure()
param portalDefinition object

param existingOpenAiInstance object = {
  name: ''
  subscriptionId: ''
  resourceGroup: ''
}


var deployOpenAi = empty(existingOpenAiInstance.name)
var azureOpenAiEndpoint = deployOpenAi ? openAi.outputs.endpoint : customerOpenAi.properties.endpoint
var azureOpenAi = deployOpenAi ? openAiInstance : existingOpenAiInstance
var openAiInstance = {
  name: openAi.outputs.name
  resourceGroup: rg.name
  subscriptionId: subscription().subscriptionId
}

// Tags that should be applied to all resources.
// 
// Note that 'azd-service-name' tags should be applied separately to service host resources.
// Example usage:
//   tags: union(tags, { 'azd-service-name': <service name in azure.yaml> })
var tags = {
  'azd-env-name': environmentName
}

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location, resourceGroupName))

targetScope = 'subscription'
resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: '${resourceGroupName}'
  location: location
  tags: tags
}

resource customerOpenAiResourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' existing =
  if (!deployOpenAi) {
    scope: subscription(existingOpenAiInstance.subscriptionId)
    name: existingOpenAiInstance.resourceGroup
  }

resource customerOpenAi 'Microsoft.CognitiveServices/accounts@2023-05-01' existing =
  if (!deployOpenAi) {
    name: existingOpenAiInstance.name
    scope: customerOpenAiResourceGroup
  }

module keyVault './shared/keyvault.bicep' = {
  name: 'keyvault'
  params: {
    location: location
    tags: tags
    name: '${abbrs.keyVaultVaults}${resourceToken}'
    principalId: principalId
  }
  scope: rg
}

module monitoring './shared/monitoring.bicep' = {
  name: 'monitoring'
  params: {
    keyvaultName: keyVault.outputs.name
    location: location
    tags: tags
    logAnalyticsName: '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    applicationInsightsName: '${abbrs.insightsComponents}${resourceToken}'
  }
  scope: rg
}

module registry './shared/registry.bicep' = {
  name: 'registry'
  params: {
    location: location
    tags: tags
    name: '${abbrs.containerRegistryRegistries}${resourceToken}'
  }
  scope: rg
}

module appsEnv './shared/apps-env.bicep' = {
  name: 'apps-env'
  params: {
    name: '${abbrs.appManagedEnvironments}${resourceToken}'
    location: location
    tags: tags //union(tags, { 'azd-service-name': 'web' })
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    logAnalyticsWorkspaceName: monitoring.outputs.logAnalyticsWorkspaceName
  }
  scope: rg
}


module userPortalApp './app/UserPortal.bicep' = {
  name: 'UserPortal'
  params: {
    name: '${abbrs.appContainerApps}portal-${resourceToken}'
    location: location
    tags: tags
    keyvaultName: keyVault.outputs.name
    identityName: '${abbrs.managedIdentityUserAssignedIdentities}portal-${resourceToken}'
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    containerAppsEnvironmentName: appsEnv.outputs.name
    containerRegistryName: registry.outputs.name
    exists: userPortalExists
    appDefinition: portalDefinition
    envSettings: [
      {
        name: 'SERVICE_API_ENDPOINT_URL'
        value: apiApp.outputs.uri
      }
    ]
    secretSettings: [
      {
        name: 'ApplicationInsights__ConnectionString'
        value: monitoring.outputs.applicationInsightsConnectionSecretRef
        secretRef: monitoring.outputs.applicationInsightsConnectionSecretName
      }
    ]
  }
  scope: rg
  dependsOn: [ apiApp, monitoring ]
}

module apiApp './app/API.bicep' = {
  name: 'API'
  params: {
    name: '${abbrs.appContainerApps}api-${resourceToken}'
    location: location
    tags: tags
    keyvaultName: keyVault.outputs.name
    identityName: '${abbrs.managedIdentityUserAssignedIdentities}api-${resourceToken}'
    storageAccountName: storage.outputs.name
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    containerAppsEnvironmentName: appsEnv.outputs.name
    containerRegistryName: registry.outputs.name
    exists: userPortalExists
    appDefinition: portalDefinition
    openAIServiceName: openAi.outputs.name
    envSettings: [
      {
        name: 'AZURE_KEY_VAULT_NAME'
        value: keyVault.outputs.name
      }
    ]
    secretSettings: [
      {
        name: 'ApplicationInsights__ConnectionString'
        value: monitoring.outputs.applicationInsightsConnectionSecretRef
        secretRef: monitoring.outputs.applicationInsightsConnectionSecretName
      }
    ]
  }
  scope: rg
  dependsOn: [ monitoring, keyVault ]
}

module apiAppPostgresqlAdmin './shared/postgresql_administrator.bicep' = {
  name: 'apiAppPostgresqlAdmin'
  params: {
    postgresqlServerName: postgresql.outputs.serverName
    principalId: apiApp.outputs.identityPrincipalId
    principalName: apiApp.outputs.identityPrincipalName
  }
  scope: rg
}

module openAi './shared/openai.bicep' = if (deployOpenAi) {
  name: 'openai'
  params: {
    deployments: [
      {
        name: 'completions'
        sku: {
          name: 'Standard'
          capacity: 10
        }
        model: {
          name: 'gpt-4o'
          version: '2024-05-13'
        }
      }
      {
        name: 'embeddings'
        sku: {
          name: 'Standard'
          capacity: 10
        }
        model: {
          name: 'text-embedding-3-large'
          version: '1'
        }
      }
    ]
    keyvaultName: keyVault.outputs.name
    location: location
    name: '${abbrs.openAiAccounts}${resourceToken}'
    sku: 'S0'
    tags: tags
  }
  scope: rg
}

module openAiSecrets './shared/openai-secrets.bicep' = {
  name: 'openaiSecrets'
  params: {
    keyvaultName: keyVault.outputs.name
    openAiInstance: azureOpenAi
    tags: tags
  }
  scope: rg
}

module postgresql './shared/postgresql.bicep' = {
  name: 'postgresql'
  params: {
    location: location
    serverName: '${abbrs.dBforPostgreSQLServers}data${resourceToken}'
    skuName: 'Standard_B2ms'
    skuTier: 'Burstable'
    highAvailabilityMode: 'Disabled'
    administratorLogin: postgresqlAdminLogin
    administratorLoginPassword: postgresqlAdminPassword
    databaseName: postgresqlDatabaseName
    tags: tags
    keyvaultName: keyVault.outputs.name
  }
  scope: rg
}


module storage './shared/storage.bicep' = {
  name: 'storage'
  params: {
    containers: [
      {
        name: 'documents'
      }
    ]
    files: []
    keyvaultName: keyVault.outputs.name
    location: location
    name: '${abbrs.storageStorageAccounts}${resourceToken}'
    tags: tags
  }
  scope: rg
}


output AZURE_RESOURCE_GROUP string = rg.name
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = registry.outputs.loginServer
output AZURE_KEY_VAULT_NAME string = keyVault.outputs.name
output AZURE_KEY_VAULT_ENDPOINT string = keyVault.outputs.endpoint
output AZURE_STORAGE_ACCOUNT_NAME string = storage.outputs.name

output POSTGRESQL_SERVER_NAME string = postgresql.outputs.serverName
output POSTGRESQL_DATABASE_NAME string = postgresqlDatabaseName

output SERVICE_API_IDENTITY_PRINCIPAL_NAME string = apiApp.outputs.identityPrincipalName

output SERVICE_USERPORTAL_ENDPOINT_URL string = userPortalApp.outputs.uri
output SERVICE_API_ENDPOINT_URL string = apiApp.outputs.uri
