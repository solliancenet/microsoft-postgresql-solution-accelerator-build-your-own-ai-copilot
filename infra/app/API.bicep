param name string
param location string = resourceGroup().location
param tags object = {}

param appConfigName string
param identityName string
param storageAccountName string
param containerRegistryName string
param containerAppsEnvironmentName string
param applicationInsightsName string
param documentIntelligenceName string
param exists bool
@secure()
param appDefinition object
param envSettings array = []
param secretSettings array = []
param openAIServiceName string

var appSettingsArray = filter(array(appDefinition.settings), i => i.name != '')
var secrets = union(map(filter(appSettingsArray, i => i.?secret != null), i => {
  name: i.name
  value: i.value
  secretRef: i.?secretRef ?? take(replace(replace(toLower(i.name), '_', '-'), '.', '-'), 32)
}), secretSettings)

var env = union(map(filter(appSettingsArray, i => i.?secret == null), i => {
  name: i.name
  value: i.value
}), envSettings)

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2022-02-01-preview' existing = {
  name: containerRegistryName
}

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-04-01-preview' existing = {
  name: containerAppsEnvironmentName
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' existing = {
  name: storageAccountName
}

resource openAIService 'Microsoft.CognitiveServices/accounts@2023-05-01' existing = {
  name: openAIServiceName
}

resource docIntelligence 'Microsoft.CognitiveServices/accounts@2024-06-01-preview' existing = {
  name: documentIntelligenceName
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  scope: docIntelligence
  name: guid(resourceGroup().id, identity.id, 'Cognitive Services Face Recognizer')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '9894cab4-e18a-44aa-828b-cb588cd6f2d7') // Cognitive Services Face Recognizer role
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource apiAppRoleAssignment 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  scope: openAIService
  name: guid(subscription().id, resourceGroup().id, identity.id, 'Cognitive Services OpenAI User')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd') // Cognitive Services OpenAI User role ID
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource apiAppOpenAIContributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  scope: openAIService
  name: guid(subscription().id, resourceGroup().id, identity.id, 'Cognitive Services OpenAI Contributor')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'a001fd3d-188f-4b5d-821b-7da978bf7442') // Cognitive Services OpenAI Contributor role ID
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: containerRegistry
  name: guid(subscription().id, resourceGroup().id, identity.id, 'acrPullRole')
  properties: {
    roleDefinitionId:  subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d') // ACR Pull role
    principalType: 'ServicePrincipal'
    principalId: identity.properties.principalId
  }
}

resource storageBlobDataContributorRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: guid(subscription().id, resourceGroup().id, identity.id, 'storageBlobDataContributorRole')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe') // Storage Blob Data Contributor role
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource appConfig 'Microsoft.AppConfiguration/configurationStores@2024-05-01' existing = {
  name: appConfigName
}

resource appConfigRoleAssignment 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(subscription().id, resourceGroup().id, identity.id, 'AppConfigDataReader')
  scope: appConfig
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '516239f1-63e1-4d78-a4de-a74fb236a071') // App Configuration Data Reader role
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource appConfigDocIntelligenceEndpoint 'Microsoft.AppConfiguration/configurationStores/keyValues@2024-05-01' = {
  parent: appConfig
  name: 'doc-intelligence-endpoint'
  properties: {
    value: docIntelligence.properties.endpoints.FormRecognizer
  }
}


module fetchLatestImage '../shared/fetch-container-image.bicep' = {
  name: '${name}-fetch-image'
  params: {
    exists: exists
    name: name
  }
}

resource app 'Microsoft.App/containerApps@2023-04-01-preview' = {
  name: name
  location: location
  tags: union(tags, {'azd-service-name':  'API' })
  dependsOn: [ acrPullRole ]
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identity.id}': {} }
  }
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      ingress:  {
        external: true
        targetPort: 80
        transport: 'auto'
      }
      registries: [
        {
          server: '${containerRegistryName}.azurecr.io'
          identity: identity.id
        }
      ]
      secrets: union([
      ],
      map(secrets, secret => {
        identity: identity.id
        keyVaultUrl: secret.value
        name: secret.secretRef
      }))
    }
    template: {
      containers: [
        {
          image: fetchLatestImage.outputs.?containers[?0].?image ?? 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
          name: 'main'
          env: union([
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: applicationInsights.properties.ConnectionString
            }
            {
              name: 'PORT'
              value: '80'
            }
            {
              name: 'AZURE_CLIENT_ID'
              value: identity.properties.clientId
            }
            {
              name: 'AZURE_IDENTITY_NAME'
              value: identity.name
            }
            {
              name: 'AZURE_APP_CONFIG_ENDPOINT'
              value: appConfig.properties.endpoint
            }
          ],
          env,
          map(secrets, secret => {
            name: secret.name
            secretRef: secret.secretRef
          }))
          resources: {
            cpu: json('1.0')
            memory: '2.0Gi'
          }
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 10
      }
    }
  }
}

output defaultDomain string = containerAppsEnvironment.properties.defaultDomain
output name string = app.name
output uri string = 'https://${app.properties.configuration.ingress.fqdn}'
output id string = app.id
output identityPrincipalId string = identity.properties.principalId
output identityPrincipalName string = identity.name
