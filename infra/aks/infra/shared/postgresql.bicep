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
param version string = '14'

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

@description('The subnet ID for the PostgreSQL server.')
param subnetId string = ''

@description('Name for DNS Private Zone when connecting to Subnet')
param dnsZoneName string = '${serverName}'

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
    } : {}
  }
  tags: tags
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

resource secretServer 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  name: 'postgresql-server'
  parent: keyvault
  tags: tags
  properties: {
    value: postgresqlServer.properties.fullyQualifiedDomainName
  }
}

resource secretConnectionString 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  name: 'postgresql-connection'
  parent: keyvault
  tags: tags
  properties: {
    value: 'postgresql://${administratorLogin}:${administratorLoginPassword}@${postgresqlServer.properties.fullyQualifiedDomainName}:5432/${databaseName}'
  }
}

output serverName string = postgresqlServer.name
output fqdn string = postgresqlServer.properties.fullyQualifiedDomainName
output databaseName string = postgresqlDatabase.name

output postgresqlConnectionStringSecretRef string = '${keyvault.name}.vault.azure.net/secrets/${secretConnectionString.name}'
output postgresqlConnectionStringSecretName string = secretConnectionString.name
