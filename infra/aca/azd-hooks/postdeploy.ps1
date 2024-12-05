az account set --subscription ${env:AZURE_SUBSCRIPTION_ID}

Write-Host "Get Database Password from Key Vault"
export SECRET_VALUE=$(az keyvault secret show --vault-name ${env:AZURE_KEY_VAULT_NAME} --name "postgresql-adminpassword" --query value -o tsv)


Write-Host "Install 'azure_ai' extension in PostgreSQL database"
psql -h ${env:POSTGRESQL_DATABASE_NAME}.postgres.database.azure.com -U ${env:POSTGRESQL_ADMIN_LOGIN} -d ${env:POSTGRESQL_DATABASE_NAME} -c "CREATE EXTENSION azure_ai"

