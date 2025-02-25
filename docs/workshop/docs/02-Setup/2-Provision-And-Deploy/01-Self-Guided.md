# Self-Guided Setup

Welcome to the Self-Guided Lab Track! You will need a valid Azure subscription, a GitHub account, and access to relevant Azure OpenAI models to complete this lab. Review the [prerequisites](../../0-Prerequisites/#self-guided) section if you need more details.

!!! question "WERE YOU LOOKING FOR THE INSTRUCTOR-LED OPTION INSTEAD? [You can find that here.](./02-Instructor-Led.md)"

## Authenticate With Azure

Before running the `azd up` command, you must authenticate your VS Code environment to Azure.

1. To create Azure resources, you need to be authenticated from VS Code. Open a new integrated terminal in VS Code. Then, complete the following steps:

### Step 1: Authenticate with `az` for post-provisioning tasks

1. Log into the Azure CLI `az` using the command below.

    ```bash  title=""
    az login
    ```

2. Complete the login process in the browser window that opens.

    !!! info "If you have more than one Azure subscription, you may need to run `az account set -s <subscription-id>` to specify the correct subscription to use."

### Step 2: Authenticate with `azd` for provisioning & managing resources

1. Log in to Azure Developer CLI. This is only required once per-install.

    ```bash title=""
    azd auth login
    ```

## Provision Azure Resource and Deploy App (UI and API)

You are now ready to provision your Azure resources and deploy the Woodgrove back solution.

1. Use `azd up` to provision your Azure infrastructure and deploy the web application to Azure.

    ```bash title=""
    azd up
    ```

    !!! info "You will be prompted for several inputs for the `azd up` command:"

        - **Enter a new environment name**: Enter a value, such as `dev`.
        - The environment for the `azd up` command ensures configuration files, environment variables, and resources are provisioned and deployed correctly.
        - Should you need to delete the `azd` environment, locate and delete the `.azure` folder at the root of the project in the VS Code Explorer.
        - **Select an Azure Subscription to use**: Select the Azure subscription you are using for this workshop using the up and down arrow keys.
        - **Select an Azure location to use**: Select the Azure region into which resources should be deployed using the up and down arrow keys.
        - **Enter a value for the `deployAMLModel`**: Select `True` if you were able to ensure you have sufficient Azure ML CPU quota available to deploy the model. Otherwise, choose `False`.
        - If you select `False`, you will need to skip the optional **Semantic Ranker** section of this accelerator.
        - **Enter a value for the `resourceGroupName`**: Enter `rg-postgresql-accelerator`, or a similar name.

2. Wait for the process to complete. It may take 30-45 minutes or more.

    !!! failure "Not enough subscription CPU quota"

        If you did not check your Azure ML CPU quota prior to starting running the `azd up` command, you may receive a CPU quota error message similar to the following:

        _(OutOfQuota) Not enough subscription CPU quota. The amount of CPU quota requested is 32 and your maximum amount of quota is [N/A]. Please see troubleshooting guide, available here: https://aka.ms/oe-tsg#error-outofquota_

        You can still continue with the workshop, but will need to skip the optional **Semantic Ranking** section, as you will not have the deployed model available.

    !!! failure "Deployment failed: Postgresql server is not in an accessible state"

        It's possible a `server is not in an accessible state` error may occur when the Azure Bicep deployment attempts to add the PostgreSQL Admin User after the PostgreSQL Server has been provisioned. This can occur if the PostgreSQL server is still being provisioned in the Azure backend, but the Deployment returned that it's successful already. If you encounter this error, simply re-run the `azd up` command.

        ```
        ERROR: error executing step command 'provision': deployment failed: error deploying infrastructure: deploying to subscription:

        Deployment Error Details:
        AadAuthOperationCannotBePerformedWhenServerIsNotAccessible: The server 'psql-datacvdjta5pfnc5e' is not in an accessible state to perform Azure AD Principal operation. Please make sure the server is accessible before executing Azure AD Principal operations.
        ```
        

3. On successful completion you will see a `SUCCESS: ...` message on the console.

---

## Next → [Validate Your Setup](../3-Validation/index.md)
