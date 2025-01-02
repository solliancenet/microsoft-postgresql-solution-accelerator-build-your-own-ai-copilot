az account set --subscription ${env:AZURE_SUBSCRIPTION_ID}

az extension add -y -n "rdbms-connect"

$username=(az account show -o tsv --query "user.name")
$token=(az account get-access-token --resource=https://ossrdbms-aad.database.windows.net -o tsv --query "accessToken")

# Add local Public IP Address to PostgreSQL Firewall, so that we can connect to the PostgreSQL Server and run scripts
$publicIpAddress =  (Invoke-RestMethod -Uri "http://ipinfo.io/ip")
az postgres flexible-server firewall-rule create `
    --resource-group "${env:AZURE_RESOURCE_GROUP}" `
    --name "${env:POSTGRESQL_SERVER_NAME}" `
    --rule-name "AllowAZDLocalMachine" `
    --start-ip-address $publicIpAddress `
    --end-ip-address $publicIpAddress

# Add account running AZD as Administrator on PostgreSQL Server, so that we can run scripts
az postgres flexible-server ad-admin create `
    --resource-group "${env:AZURE_RESOURCE_GROUP}" `
    --server-name "${env:POSTGRESQL_SERVER_NAME}" `
    --display-name "$username" `
    --object-id "$(az ad user show --id $username --query id -o tsv)"



# Run Scripts

$query = "DO $`$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_user WHERE usename = '${env:SERVICE_API_IDENTITY_PRINCIPAL_NAME}') THEN
    EXECUTE format('GRANT ALL PRIVILEGES ON DATABASE %I TO %I', current_database(), '${env:SERVICE_API_IDENTITY_PRINCIPAL_NAME}');
    EXECUTE format('GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO %I', '${env:SERVICE_API_IDENTITY_PRINCIPAL_NAME}');
  END IF;
END $`$;"

az postgres flexible-server execute `
          --admin-user "$username" `
          --admin-password "$token" `
          --name "${env:POSTGRESQL_SERVER_NAME}" `
          --database-name "${env:POSTGRESQL_DATABASE_NAME}" `
          --querytext $query
          # --file-path "./scripts/grant-database-access-to-api-identity.sql"

az postgres flexible-server execute `
          --admin-user "$username" `
          --admin-password "$token" `
          --name "${env:POSTGRESQL_SERVER_NAME}" `
          --database-name "${env:POSTGRESQL_DATABASE_NAME}" `
          --file-path "./scripts/setup-semantic-ranker.sql"


$query = @"
select azure_ai.set_setting('azure_openai.endpoint', '${env:AZURE_OPENAI_ENDPOINT}');
select azure_ai.set_setting('azure_openai.subscription_key', '${env:AZURE_OPENAI_KEY}');
"@

az postgres flexible-server execute `
          --admin-user "$username" `
          --admin-password "$token" `
          --name "${env:POSTGRESQL_SERVER_NAME}" `
          --database-name "${env:POSTGRESQL_DATABASE_NAME}" `
          --querytext $query
