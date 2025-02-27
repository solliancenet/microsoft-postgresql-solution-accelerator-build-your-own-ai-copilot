# 1.3 Azure Cost Estimate

The Microsoft Azure resources you deploy will be provisioned within your Azure Subscription. You are responsible for the cost of those services. The cost of the solution will vary depending on the Azure region selected and which deployment options you choose.

Most notably, the `deployAMLModel` option you will specify during deployment will impact the overall cost:

- By deploying the Azure Machine Learning model for Semantic Ranker by setting this option to `TRUE`, the solution will cost approximately $25 per day.
- Deploying without Azure Machine Learning model for Semantic Ranker lowers the cost to approximately $5.50 daily.

The Setup section of this guide will tell you how to choose this deployment option.

Here's a breakout of the _estimated cost_ of Azure resources deployed for this solution:

- Azure ML VM (semantic ranking model deployment): ~$19.50/day
- Azure Database for PostgreSQL: ~$3.40/day
- Azure App Configuration: ~$1.20/day
- Azure Container Registry: ~$0.67/day
- Azure OpenAI Service: Dependent upon usage of Copilot, AI-validation, and number of documents processed in the solution.
- Other services are minimal cost.

![Screenshot of Cost analysis within the Azure Portal for the solution resource group.](../img/azure-cost-analysis.png)

!!! warning "The above costs are only estimates."

    The costs provided here are estimates based on running the solution accelerator using the provided configuration and are intended to provide general guidance about the costs associated with running the solution accelerator. Depending on deployment options, region selection, and data sizes, individual costs will vary.
