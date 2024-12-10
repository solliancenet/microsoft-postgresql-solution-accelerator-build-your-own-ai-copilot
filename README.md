# PostgreSQL Solution Accelerator: Build your own AI Copilot / FSI Scenario

## Solution Architecture

The solution architecture is represented by this diagram:

[TODO]

## Get Started

To deploy the solution follow the Deployment steps below.

### Deployment

This solution deploys to either Azure Kubernetes Service (**AKS**) or Azure Container Apps (**ACA**). The deployment scripts are located in the `infra/aks` and `infra/aca` folders. They are designed to be run from these dedicated folders, so you need to make sure your current working directory is properly set. To deploy the solution, run the following commands from the root of the repository:

#### ACA deployment

```bash
cd ./infra/aca
azd up
```

After running `azd up` on the **ACA** deployment and the deployment finishes, you can locate the URL of the web application by navigating to the deployed resource group in the Azure portal. Click on the link to the new resource group in the output of the script to open the Azure portal.

#### AKS deployment

```bash
cd ./infra/aks
azd up
```

After running `azd up` on the **AKS** deployment and the deployment finishes, you will see the output of the script which will include the URL of the web application. You can click on this URL to open the web application in your browser. The URL is beneath the "Done: Deploying service web" message, and is the second endpoint (the Ingress endpoint of type `LoadBalancer`).

If you closed the window and need to find the external IP address of the service, you can open the Azure portal, navigate to the resource group you deployed the solution to, and open the AKS service. In the AKS service, navigate to the `Services and Ingress` blade, and you will see the external IP address of the LoadBalancer service, named `nginx`.

> [!NOTE]
> There are many options for deployment, including using an existing Azure OpenAI account and models. For deployment options and prerequisistes, please see [How to Deploy](./docs/deployment.md) page.

Before moving to the next section, be sure to validate the deployment is successful. More information can be found in the [How to Deploy](./docs/deployment.md) page.

## Clean-up

From a command prompt, navigate to the `aks` or `aca` folder, depending on which deployment type you used, and run the following command to delete the resources created by the deployment script:

### AKS clean-up

```bash
cd ./infra/aks
azd down --purge
```

### ACA clean-up

```bash
cd ./infra/aca
azd down --purge
```

> [!NOTE]
> The `--purge` flag purges the resources that provide soft-delete functionality in Azure, including Azure KeyVault and Azure OpenAI. This flag is required to remove all resources.
