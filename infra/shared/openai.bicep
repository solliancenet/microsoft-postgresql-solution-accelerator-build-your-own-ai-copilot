param deployments array
param location string = resourceGroup().location
param name string
param sku string = 'S0'
param tags object = {}
param keyvaultName string = ''
param appConfigName string = ''

resource openAi 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: name
  location: location
  sku: {
    name: sku
  }
  kind: 'OpenAI'
  properties: {
    customSubDomainName: name
    publicNetworkAccess: 'Enabled'
  }
  tags: tags
}

@batchSize(1)
resource openAiDeployments 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = [
  for deployment in deployments: {
    parent: openAi
    name: deployment.name
    sku: {
      capacity: deployment.sku.capacity
      name: deployment.sku.name
    }
    properties: {
      model: {
        format: 'OpenAI'
        name: deployment.model.name
        version: deployment.model.version
      }
    }
  }
]

resource keyvault 'Microsoft.KeyVault/vaults@2023-02-01' existing = if (!empty(keyvaultName)) {
  name: keyvaultName
}

resource apiKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = if (!empty(keyvaultName)) {
  name: 'openai-apikey'
  parent: keyvault
  tags: tags
  properties: {
    value: openAi.listKeys().key1
  }
}

resource appConfig 'Microsoft.AppConfiguration/configurationStores@2024-05-01' existing = if (!empty(appConfigName)) {
  name: appConfigName
}

resource appConfigOpenApiKey 'Microsoft.AppConfiguration/configurationStores/keyValues@2022-05-01' =  if (!empty(appConfigName)) {
  parent: appConfig
  name: 'openai-apikey'
  properties: {
    value: '{"uri":"https://${keyvault.name}.vault.azure.net/secrets/openai-apikey"}'
    contentType: 'application/vnd.microsoft.appconfig.keyvaultref+json;charset=utf-8'
    tags: {
      environment: 'production'
    }
  }
}

resource appConfigOpenApiName 'Microsoft.AppConfiguration/configurationStores/keyValues@2024-05-01' =  if (!empty(appConfigName)) {
  parent: appConfig
  name: 'openai-endpoint'
  properties: {
    value: openAi.properties.endpoint
    contentType: 'text/plain'
    tags: {
      environment: 'production'
    }
  }
}

output endpoint string = openAi.properties.endpoint
output name string = openAi.name
output key string = openAi.listKeys().key1
