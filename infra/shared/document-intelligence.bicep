@description('The location of the Document Intelligence resource.')
param location string

@description('The name of the Document Intelligence resource.')
param name string

@description('The SKU of the Document Intelligence resource.')
param skuName string = 'F0'

resource documentIntelligence 'Microsoft.CognitiveServices/accounts@2024-06-01-preview' = {
  name: name
  location: location
  sku: {
    name: skuName
  }
  kind: 'FormRecognizer'
  identity: {
    type: 'None'
  }
  properties: {
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    publicNetworkAccess: 'Enabled'
    customSubDomainName: name
  }
}

output name string = documentIntelligence.name
output formRecognizerEndpoint string = documentIntelligence.properties.endpoints.FormRecognizer
