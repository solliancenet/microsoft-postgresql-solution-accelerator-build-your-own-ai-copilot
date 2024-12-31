
az extension add -y -n "rdbms-connect"

# az postgres flexible-server execute `
#           --resource-group "${AZURE_RESOURCE_GROUP}" `
#           --name "${POSTGRESQL_SERVER_NAME}" `
#           --database-name "${POSTGRESQL_DATABASE_NAME}" `
#           --file-path "./scripts/grant-database-access.sql" `
#           --parameters "managed_identity_name=${SERVICE_API_IDENTITY_PRINCIPAL_NAME}"



# Write-Host "Install 'azure_ai' extension in PostgreSQL database"
# psql -h ${env:POSTGRESQL_DATABASE_NAME}.postgres.database.azure.com -U ${env:POSTGRESQL_ADMIN_LOGIN} -d ${env:POSTGRESQL_DATABASE_NAME} -c "CREATE EXTENSION azure_ai"
