# PostgreSQL Solution Accelerator: Build your own AI Copilot / FSI Scenario

#### ACA deployment

```bash
azd auth login

azd env set AZURE_SUBSCRIPTION_ID "8c924580-ce70-48d0-a031-1b21726acc1a"
azd env set AZURE_RESOURCE_GROUP "ms-postgresql-byoc"
azd env set AZURE_LOCATION "eastus2"

//export POSTGRESQL_ADMIN_PASSWORD="<your-secure-password>"
export POSTGRESQL_ADMIN_PASSWORD=$(uuidgen)

// // Find the password for existing environment within connection string
// az keyvault secret show --vault-name <key-vault-name> --name postgresql-connection --query value -o tsv)



cd ./infra/aca
azd up
```
