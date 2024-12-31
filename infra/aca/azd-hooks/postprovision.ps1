
az extension add -y -n "rdbms-connect"

$username=(az account show -o tsv --query "user.name")

$token=(az account get-access-token --resource=https://ossrdbms-aad.database.windows.net -o tsv --query "accessToken")

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
