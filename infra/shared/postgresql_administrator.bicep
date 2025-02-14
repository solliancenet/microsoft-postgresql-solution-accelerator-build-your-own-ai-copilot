param postgresqlServerName string
param principalName string
param principalId string
param principalType string = 'ServicePrincipal'
param principalTenantId string = subscription().tenantId

resource postgresql 'Microsoft.DBforPostgreSQL/flexibleServers@2024-11-01-preview' existing = {
  name: postgresqlServerName
}

resource aadadmin 'Microsoft.DBforPostgreSQL/flexibleServers/administrators@2024-11-01-preview' = {
  parent: postgresql
  name: principalId
  properties: {
    principalName: principalName
    principalType: principalType
    tenantId: principalTenantId
  }
}
