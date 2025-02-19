targetScope = 'subscription'


@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Name of the resource group')
param resourceGroupName string

@description('User Principal Name of the user or app to assign application roles')
param principalName string

@description('Determines whether to deploy the Azure Machine Learning model used for Semantic Reranking')
param deployAMLModel bool

param userPortalExists bool

param runPostDeployScript bool

@secure()
param portalDefinition object

module workshopInfra '../../infra/main.bicep' = {
  name: 'workshop-infra'
  params: {
    environmentName: environmentName
    location: location
    principalName: principalName
    userPortalExists: userPortalExists
    deployAMLModel: deployAMLModel
    runPostDeployScript: runPostDeployScript
    resourceGroupName: resourceGroupName
    portalDefinition: portalDefinition

    // The workshop deployment doesn't deploy the OpenAI models (this is manual in the guide)
    deployOpenAIModels: false
  }
}


output AZURE_RESOURCE_GROUP string = workshopInfra.outputs.AZURE_RESOURCE_GROUP
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = workshopInfra.outputs.AZURE_CONTAINER_REGISTRY_ENDPOINT
output AZURE_KEY_VAULT_NAME string = workshopInfra.outputs.AZURE_KEY_VAULT_NAME
output AZURE_KEY_VAULT_ENDPOINT string = workshopInfra.outputs.AZURE_KEY_VAULT_ENDPOINT
output AZURE_APP_CONFIG_ENDPOINT string = workshopInfra.outputs.AZURE_APP_CONFIG_ENDPOINT

output AZURE_STORAGE_ACCOUNT_NAME string = workshopInfra.outputs.AZURE_STORAGE_ACCOUNT_NAME
output AZURE_STORAGE_CONTAINER_NAME string = workshopInfra.outputs.AZURE_STORAGE_CONTAINER_NAME

output STORAGE_EVENTGRID_SYSTEM_TOPIC_NAME string = workshopInfra.outputs.STORAGE_EVENTGRID_SYSTEM_TOPIC_NAME

output POSTGRESQL_SERVER_NAME string = workshopInfra.outputs.POSTGRESQL_SERVER_NAME
output POSTGRESQL_DATABASE_NAME string = workshopInfra.outputs.POSTGRESQL_DATABASE_NAME

output AZURE_OPENAI_ENDPOINT string = workshopInfra.outputs.AZURE_OPENAI_ENDPOINT
output AZURE_OPENAI_KEY string = workshopInfra.outputs.AZURE_OPENAI_KEY

output DEPLOY_AML_MODEL bool = workshopInfra.outputs.DEPLOY_AML_MODEL
output AZURE_AML_WORKSPACE_NAME string = workshopInfra.outputs.AZURE_AML_WORKSPACE_NAME
output AZURE_AML_ENDPOINT_NAME string = workshopInfra.outputs.AZURE_AML_ENDPOINT_NAME

output SERVICE_API_IDENTITY_PRINCIPAL_NAME string = workshopInfra.outputs.SERVICE_API_IDENTITY_PRINCIPAL_NAME

output SERVICE_USERPORTAL_ENDPOINT_URL string = workshopInfra.outputs.SERVICE_USERPORTAL_ENDPOINT_URL
output SERVICE_API_ENDPOINT_URL string = workshopInfra.outputs.SERVICE_API_ENDPOINT_URL

output RUN_POSTDEPLOY_SCRIPT bool = workshopInfra.outputs.RUN_POSTDEPLOY_SCRIPT
