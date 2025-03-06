# Redeploy App to Azure

The workshop began with a _pre-provisioned_ version of the _Woodgrove Bank Contract Management_ application on Azure Container Apps. Now that you have modified elements of the app and tested them out locally, you might want to _redeploy_ the application.

Because you used `azd` for provisioning and deployment, this is as simple as calling `azd up` (to push all changes in both infrastructure and application) or running `azd deploy` if you want only to rebuild and deploy the application changes you made in this project.

!!! tip "Understand the difference between `azd up` and `azd deploy`"

    The `azd up` and `azd deploy` commands are both part of the Azure Developer CLI, but they serve different purposes:

    - `azd up` is used to package, provision, and deploy your application to Azure. It sets up the entire environment, including infrastructure and application code, from scratch. It's typically used when you're starting a new project or making significant changes to your infrastructure.

    - `azd deploy` is used to update an existing deployment. It's helpful when making iterative changes to your application without needing to re-provision the entire environment. This command is ideal for continuous development and deployment scenarios where you frequently update your application.

    In other words, use `azd up` when setting everything up from the beginning and `azd deploy` when updating an existing deployment.

## Deploy the Updated App

To deploy the updated app, follow the steps below:

1. Open a new integrated terminal in Visual Studio Code.

2. Ensure you are at the root of your repository.

3. Execute this command to deploy your application with changes.

    !!! danger "Execute the following Azure Developer CLI command!"

    ```bash title=""
    azd deploy
    ```

## Test the Deployed App

1. In the Azure portal, return to the resource group containing your resources and select the **Container app** resource whose name begins with **ca-portal**.

    ![Screenshot of the resources in the resource group, with the ca-portal Container app resource highlighted.](../img/azure-portal-rg-ca-portal.png)

2. In the **Essentials** section of the Portal Container App's **Overview** page, select the **Application Url** to open the deployed Woodgrove Bank Portal in a new browser tab.

    ![Screenshot of the API container app page in the Azure portal, with the Application Url highlighted.](../img/azure-portal-portal-container-app.png)

3. In the _Woodgrove Bank Contract Management Portal_, select the **Dashboard** page and use the copilot to ask a few questions and verify that your app changes are live!

---

_You made it! That was a lot to cover - but don't worry! Now that you have a fork of the repo, you can revisit ideas at your own pace! Before you go, there are some important cleanup tasks you need to do!!_

---

!!! note "THANK YOU: Let's wrap up the session by cleaning up resources!"
