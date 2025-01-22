@description('The location of the PostgreSQL server.')
param location string

@description('The name of the PostgreSQL server.')
param serverName string

@description('The administrator username for the PostgreSQL server.')
param administratorLogin string

@secure()
@description('The administrator password for the PostgreSQL server.')
param administratorLoginPassword string

@description('The name of the PostgreSQL database.')
param databaseName string

@description('The SKU name for the PostgreSQL server.')
param skuName string = 'Standard_D2ds_v4'

@description('The tier for the PostgreSQL server.')
@allowed([
  'GeneralPurpose'
  'MemoryOptimized'
  'Burstable'
])
param skuTier string = 'GeneralPurpose'

@description('The version of the PostgreSQL server.')
param version string = '16'

@description('Azure database for PostgreSQL storage Size ')
param storageSizeGB int = 32

@description('PostgreSQL Server backup retention days')
param backupRetentionDays int = 7

@description('Geo-Redundant Backup setting')
param geoRedundantBackup string = 'Disabled'

@description('The tags to apply to the resources.')
param tags object

@description('The name of the key vault to store the connection string.')
param keyvaultName string

@description('The name of the app config to store the connection string.')
param appConfigName string

@description('The subnet ID for the PostgreSQL server.')
param subnetId string = ''

@description('Name for DNS Private Zone when connecting to Subnet')
param dnsZoneName string = serverName

@description('Fully Qualified DNS Private Zone')
param dnsZoneFqdn string = '${dnsZoneName}.postgres.database.azure.com'

@description('High Availability Mode')
@allowed([
  'ZoneRedundant'
  'Disabled'
])
param highAvailabilityMode string = 'Disabled'

var connectSubnet = !empty(subnetId)

resource dnszone 'Microsoft.Network/privateDnsZones@2020-06-01' = if (connectSubnet) {
  name: dnsZoneFqdn
  location: 'global'
}

resource postgresqlServer 'Microsoft.DBforPostgreSQL/flexibleServers@2024-08-01' = {
  name: serverName
  location: location
  sku: {
    name: skuName
    tier: skuTier
  }
  properties: {
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
    authConfig: {
      activeDirectoryAuth: 'Enabled'
      passwordAuth: 'Enabled'
      tenantId: subscription().tenantId
    }
    storage: {
      storageSizeGB: storageSizeGB  
    }
    createMode: 'Default'
    version: version
    backup: {
      backupRetentionDays: backupRetentionDays
      geoRedundantBackup: geoRedundantBackup
    }
    highAvailability: {
      mode: highAvailabilityMode
    }
    network: connectSubnet ?{
      delegatedSubnetResourceId: subnetId
      privateDnsZoneArmResourceId: dnszone.id
      publicNetworkAccess: 'Enabled'
    } : {
      publicNetworkAccess: 'Enabled'
    }
  }
  tags: tags
}

resource firewallRuleAllowAzureIPs 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-12-01-preview' = {
  parent: postgresqlServer
  name: 'AllowAllAzureServicesAndResourcesWithinAzureIps'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// Enable these extensions for the PostgreSQL server
resource postgresqlExtensions 'Microsoft.DBforPostgreSQL/flexibleServers/configurations@2024-11-01-preview' = {
  parent: postgresqlServer
  name: 'azure.extensions'
  properties: {
    source: 'user-override'
    value: 'AZURE_AI,VECTOR'
  }
}

resource postgresqlDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2024-08-01' = {
  name: databaseName
  parent: postgresqlServer
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

resource keyvault 'Microsoft.KeyVault/vaults@2023-02-01' existing = {
  name: keyvaultName
}

resource secretAdminUser 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  name: 'postgresql-adminuser'
  parent: keyvault
  tags: tags
  properties: {
    value: administratorLogin
  }
}

resource secretAdminPassword 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  name: 'postgresql-adminpassword'
  parent: keyvault
  tags: tags
  properties: {
    value: administratorLoginPassword
  }
}

resource appConfig 'Microsoft.AppConfiguration/configurationStores@2024-05-01' existing = if (!empty(appConfigName)) {
  name: appConfigName
}

resource appConfigPostgresqlServerName 'Microsoft.AppConfiguration/configurationStores/keyValues@2024-05-01' = if (!empty(appConfigName)) {
  parent: appConfig
  name: 'postgresql-server'
  properties: {
    value: postgresqlServer.properties.fullyQualifiedDomainName
  }
}

resource appConfigPostgresqlDatabaseName 'Microsoft.AppConfiguration/configurationStores/keyValues@2024-05-01' = if (!empty(appConfigName)) {
  parent: appConfig
  name: 'postgresql-database'
  properties: {
    value: postgresqlDatabase.name
  }
}

output serverName string = postgresqlServer.name
output fqdn string = postgresqlServer.properties.fullyQualifiedDomainName
output databaseName string = postgresqlDatabase.name
