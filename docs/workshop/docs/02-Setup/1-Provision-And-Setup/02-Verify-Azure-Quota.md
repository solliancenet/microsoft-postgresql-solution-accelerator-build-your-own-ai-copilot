# Verify Azure Quota

This solution contains an Azure Developer CLI `azd-template` that provisions the required resources in Azure and deploys the starter app to Azure Container Apps (ACA). The template allows for the infrastructure to be deployed with a single `azd up` command. On completing this step, you should have:

- [X] Selected an Azure region for workshop resources
- [X] Verified your Azure ML CPU quota
- [X] Authenticated with Azure
- [X] Provisioned Azure resources and deployed the starter solution

## Select an Azure region for your workshop resources

To ensure you can successfully deploy the Azure resources using the `azd up` command, you must choose a region that supports the required Azure OpenAI `gpt-4o` and `text-embedding-ada-002` models.

1. Before deciding on the Azure region you want to use for your workshop resources:

    1. Review the regional availability guidance for the [gpt-4o](https://learn.microsoft.com/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#standard-models-by-endpoint) and [text-embedding-ada-002](https://learn.microsoft.com/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-embeddings#standard-models-by-endpoint) models in Azure OpenAI.

    2. Check the [text abstractive summarization regional availability](https://learn.microsoft.com/azure/ai-services/language-service/summarization/region-support#regional-availability-table)

2. Choose a region that **supports both Azure OpenAI models** and **Text Abstractive Summarization**.

!!! danger "Select a region that supports Azure OpenAI both models!"

Choosing a region that doesn't support both Azure OpenAI models will result in deployment failure when running `azd up`.

Selecting a region that does not support _abstractive summarization_ will not cause a deployment failure, but will need to make code changes later in the workshop to use _extractive summarization_ in its place.

## Verify Azure ML CPU Quota

This solution accelerator contains a section dedicted to setting up and using a Semantic Ranking model directly from your PostgreSQL database. The deployment of this component of the architecture requires sufficient CPU quota (32 cores) in Azure Machine Learning to accomodate the [Hugging Face BGE reranker model deployment](https://huggingface.co/BAAI/bge-reranker-v2-m3). In this task, you must verify you have available quota for the target virtual machine (VM) instance type (`STANDARD_D16AS_V4`), and if not, request additional quota.

1. To view your available quota, you first need to retrieve your Microsoft Entra ID **Tenant ID** from the [Azure portal](https://portal.azure.com/).

2. In the Azure portal, enter "Microsoft Entra ID" into the search bar, then select **Microsoft Entra ID** from the **Services** list in the results.

    ![Microsoft Entra ID is entered into the Azure search bar and it is highlighted in the Services results.](../../img/azure-portal-search-entra-id.png)

3. On the **Overview** page of your Microsoft Entra ID tenant, select the **Copy to clipboard** button for your **Tenant ID**.

    ![On the Entra ID tenant overview tab, the copy to clipboard button for the Tenant ID is highlighted with a red box.](../../img/azure-portal-entra-id-tenant-overview.png)

4. Open a new browser window or tab and navigate to the following URL, replacing the `<your-tenant-id>` token with the Tenant ID you copied from the Entra ID overview page in the Azure portal.

    ```bash title="Azure ML Quota page"
    https://ml.azure.com/quota?tid=<your-tenant-id>
    ```

5. On the Azure ML **Quota** page, select the subscription you are using for this workshop.

    ![Screenshot of the Azure ML quota subscription selection page.](../../img/azure-ml-quota-subscription.png)

6. On the quota page for your selected subscription, select the Azure region you plan to use for this workshop. This should be the region you chose in previous task that supports the required Azure OpenAI models.

7. You should now see a list of CPUs and their quotas within your subscription. Locate **Standard DASv4 Family Cluster Dedicated vCPUs** in the list and inspect the **Quota** available.
    
    ![On the subscription quota page for the selected region, the Standard DASv4 Family Cluster Dedicated vCPUs items is highlighted and the available quota is highlighted.](../../img/azure-ml-quota-standard-dasv4.png)

8. If you have 32 cores or more available, you can skip to the [Authenticate With Azure task](#33-authenticate-with-azure). Otherwise, select the **Standard DASv4 Family Cluster Dedicated vCPUs** by checking the box to the left of the name, then scroll up to the top of the page and locate the **Request quota** button.

    ![Screenshot of the Azure ML quota page with the Request quota button highlighted with a red box.](../../img/azure-ml-request-quota.png)

9. In the **Request quota** dialog, increase your **New cores limit** value by 32 and then select **Submit**.

    ![Screenshot of the Request quota dialog with a value of 32 highlighted in the new cores limit box and the submit button highlighted.](../../img/azure-ml-request-quota-dialog.png)

    !!! example

        Your **new cores limit** should be increased to ensure 32 cores are available for a new deployment. For example, if you have zero cores available, your new cores limit should be set to 32. If your core limit is 100 and you are currently using 90, your new cores limit should be set to 122.

10. Quota increase requests typically take a few minutes to complete. You will recieve notifications in the Azure portal as the request is processed and when it completes.

11. If your request is denied, you don't have permissions to issue the request, or you prefer not to request additional quota, you have the option to exclude the **Semantic Ranking** model deployment when running the `azd up` command by setting the `deployAMLModel` flag to `false` when prompted.

=== "Self-Guided"

    !!! info "You need to provision the infrastructure yourself! [Jump to the Self-Guided section](./03-Self-Guided.md) now!"  

=== "Instructor-Led"

    !!! info "You will be provisioning the infrastructure during an Instructor-Led Workshop! [Jump ahead to Instructor-Led section.](./04-Instructor-Led.md)"

    <!-- !!! info "You will use a pre-provisioned VM from Skillable! [Jump ahead to the Instructor-Led section.](./04-Instructor-Led.md)" -->
