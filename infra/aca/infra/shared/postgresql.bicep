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
param skuName string = 'B_Gen5_1'

@description('The tier for the PostgreSQL server.')
param skuTier string = 'Basic'

@description('The capacity of the PostgreSQL server.')
param skuCapacity int = 1

@description('The family of the PostgreSQL server.')
param skuFamily string = 'Gen5'

@description('The version of the PostgreSQL server.')
param version string = '11'

@description('The tags to apply to the resources.')
param tags object

resource postgresqlServer 'Microsoft.DBforPostgreSQL/servers@2017-12-01' = {
  name: serverName
  location: location
  sku: {
    name: skuName
    tier: skuTier
    capacity: skuCapacity
    family: skuFamily
  }
  properties: {
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
    version: version
    storageProfile: {
      storageMB: 5120
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
      storageAutogrow: 'Enabled'
    }
  }
  tags: tags
}

resource postgresqlDatabase 'Microsoft.DBforPostgreSQL/servers/databases@2017-12-01' = {
  name: '${serverName}/${databaseName}'
  properties: {
    charset: 'UTF8'
    collation: 'English_United States.1252'
  }
  tags: tags
}

output postgresqlServerName string = postgresqlServer.name
output postgresqlServerFullyQualifiedDomainName string = postgresqlServer.properties.fullyQualifiedDomainName
output postgresqlDatabaseName string = postgresqlDatabase.name
