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

@description('Administrator Password for the PostgreSQL server')
@secure()
param postgresqlAdminPassword string

@description('Id of the user or app to assign application roles')
param principalId string

@description('Determines whether to deploy the Azure Machine Learning model used for Semantic Reranking')
param deployAMLModel bool

param userPortalExists bool

param runPostDeployScript bool

module workshopInfra '../../infra/main.bicep' = {
  name: 'workshop-infra'
  params: {
    environmentName: environmentName
    location: location
    principalId: principalId
    userPortalExists: userPortalExists
    postgresqlAdminPassword: postgresqlAdminPassword
    deployAMLModel: deployAMLModel
    runPostDeployScript: runPostDeployScript
    resourceGroupName: resourceGroupName

    // The workshop deployment doesn't deploy the OpenAI models (this is manual in the guide)
    deployOpenAIModels: false
  }
}
