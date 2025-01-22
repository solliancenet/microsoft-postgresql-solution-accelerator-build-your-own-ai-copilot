param containers array = []
param files array = []
param appConfigName string
param location string = resourceGroup().location
param name string
param tags object = {}

resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: name
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  identity: {
    type: 'SystemAssigned'
  }
  tags: tags
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storage
  name: 'default'
}

resource blobContainers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = [
  for container in containers: {
    parent: blobService
    name: container.name
  }
]

resource blobFiles 'Microsoft.Resources/deploymentScripts@2020-10-01' = [
  for file in files: {
    name: file.file
    location: location
    kind: 'AzureCLI'
    properties: {
      azCliVersion: '2.26.1'
      timeout: 'PT5M'
      retentionInterval: 'PT1H'
      environmentVariables: [
        {
          name: 'AZURE_STORAGE_ACCOUNT'
          value: storage.name
        }
        {
          name: 'AZURE_STORAGE_KEY'
          secureValue: storage.listKeys().keys[0].value
        }
      ]
      scriptContent: 'echo "${file.content}" > ${file.file} && az storage blob upload -f ${file.file} -c ${file.container} -n ${file.path}'
    }
    dependsOn: [ blobContainers ]
  }
]

resource appConfig 'Microsoft.AppConfiguration/configurationStores@2024-05-01' existing = if (!empty(appConfigName)) {
  name: appConfigName
}

resource appConfigStorageAccountName 'Microsoft.AppConfiguration/configurationStores/keyValues@2024-05-01' = if (!empty(appConfigName)) {
  parent: appConfig
  name: 'storage-account'
  properties: {
    value: storage.name
  }
}

output name string = storage.name
output id string = storage.id
