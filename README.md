# PostgreSQL Solution Accelerator: Build your own AI Copilot / FSI Scenario

#### ACA deployment

```bash
azd auth login

azd env set AZURE_SUBSCRIPTION_ID "8c924580-ce70-48d0-a031-1b21726acc1a"
azd env set AZURE_RESOURCE_GROUP "ms-postgresql-byoc"
azd env set AZURE_LOCATION "eastus2"

cd ./infra/aca
azd up
```
