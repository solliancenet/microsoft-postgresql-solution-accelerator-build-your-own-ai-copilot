@description('Location for all resources.')
param location string = resourceGroup().location

@description('Unique name for the Azure AI Language service account.')
param name string = 'lang-${resourceGroup().location}-${uniqueString(resourceGroup().id)}'

@description('Restore the service instead of creating a new instance. This is useful if you previously soft-deleted the service and want to restore it. If you are restoring a service, set this to true. Otherwise, leave this as false.')
param restore bool = false

@description('Creates an Azure AI Language service account.')
resource languageService 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: name
  location: location
  kind: 'TextAnalytics'
  sku: {
    name: 'S'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: name
    publicNetworkAccess: 'Enabled'
    restore: restore
  } 
}

output LANGUAGE_SERVICE_NAME string = languageService.name
output LANGUAGE_SERVICE_ENDPOINT string = languageService.properties.endpoint
output LANGUAGE_SERVICE_KEY string = languageService.listKeys().key1
output LANGUAGE_SERVICE_REGION string = languageService.location
