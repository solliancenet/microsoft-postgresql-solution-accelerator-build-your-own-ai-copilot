# A. Self-Guided Setup

Welcome to the Self-Guided Lab Track! You will need a valid Azure subscription, a GitHub account, and access to relevant Azure OpenAI models to complete this lab. Review the [prerequisites](../../0-Prerequisites/#self-guided) section if you need more details.

!!! question "WERE YOU LOOKING FOR THE INSTRUCTOR-LED OPTION INSTEAD? [You can find that here.](./02-Instructor-Led.md)"

---

You will need to install the required software locally and provision the Azure infrastructure yourself, as described on the tabs below.

!!! note "Select each of the tabs below, in order"

    To complete the required setup, select the number tabs below and follow the instructions provided.

=== "1. Install software"

    The required development environment uses a Visual Studio (VS) Code editor with a Python runtime. To complete this lab on your own computer, you must install the following required software. On completing this step, you should have installed:

    - [X] Azure command-line tools
    - [X] Git
    - [X] Python 3.11+
    - [X] Node.js
    - [X] Docker desktop
    - [X] Visual Studio Code and required extensions
    - [X] pgAdmin

    ## **1.1 Install Azure command-line tools**

    !!! note "In this task, you will install both the Azure CLI and the Azure Developer CLI (`azd`)."

        - The Azure CLI enables you to execute Azure CLI commands from a command prompt or VS Code terminal on your local machine.
        - The Azure Developer CLI (`azd`) is an open-source tool that accelerates provisioning and deploying app resources on Azure.
    
    1. Download and install the latest version of the [Azure CLI](https://docs.microsoft.com/cli/azure/?view=azure-cli-latest).

    2. Once installed, open a command prompt on your machine and verify the installation by running the following:

        ```azurecli title=""
        az version
        ```

    3. Next, install the `ml` extension to the Azure CLI.
 
        !!! info "About the ml extension"

            The `ml` extension to the Azure CLI is the enhanced interface for Azure Machine Learning. It enables you to train and deploy models from the command line, with features that accelerate scaling data science up and out while tracking the model lifecycle.

        To install the `ml` extensinon you should first remove any existing installation of the extension and also the CLI v1 `azure-cli-ml` extension:
    
        ```azurecli title=""
        az extension remove -n azure-cli-ml
        az extension remove -n ml
        ```

        Then, run the following to install the latest version of the `ml` extension:
    
        ```azurecli title=""
        az extension add -n ml
        ```

    4. Install Azure Developer CLI by following the instructions for your OS at <https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd>.

    5. Execute the following command from a terminal prompt to verify the tools were installed:
        
        ```bash title=""
        azd version
        ```

    ## **1.2 Install Git**

    Git enables you to manage your code by tracking changes, maintaining a version history, and facilitating collaboration with others. This helps in organizing and maintaining the integrity of your project's development.

    1. Download Git from <https://git-scm.com/downloads>.

    2. Run the installer using the default options.

    ## **1.3 Install Python**

    Python is the programming used to build the backend API for the solution. By utilizing Python's versatile programming capabilities and Azure Database for PostgreSQL's generative AI and vector search capabilities, you can create powerful and efficient AI copilots and streamlining complex workflows.

    1. Download Python 3.11+ from <https://python.org/downloads>.

    2. Run the installer using the default options.

    3. Use the following command from a terminal prompt to verify Python was installed:

        ```bash title=""
        python --version
        ```

    ## **1.4 Install Node.js**

    Node.js is an open-source runtime environment that lets you run JavaScript code outside of a browser. It's ideal for building scalable network applications and works seamlessly with REACT single-page applications by providing a backend environment to handle server-side logic and API requests. This allows for efficient development and smooth interactions between the frontend and backend.

    1. Download Node.js from <https://nodejs.org/en/download/>, ensuring you select the most recent LTS version and your correct OS.

    2. Run the installer using the default options.

    ## **1.5 Install Docker Desktop**

    Docker Desktop is an application that allows you to build, share, and run containerized applications on your local machine. It provides a user-friendly interface to manage Docker containers, images, and networks. By streamlining the containerization process, Docker Desktop helps you develop, test, and deploy applications consistently across different environments.

    1. Download and install Docker Desktop for your OS using instructions provided on the <https://docs.docker.com/desktop/>:

           - [Linux](https://docs.docker.com/desktop/setup/install/linux/)
           - [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
           - [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)

    ## **1.6 Install Visual Studio Code (and extensions)**

    Visual Studio Code is a versatile, open-source code editor that combines powerful features with an intuitive interface to help you efficiently write, debug, and customize projects.
    
    1.  Download and install from <https://code.visualstudio.com/download>.

        - Use the default options in the installer.

    2.  After installation completed, launch Visual Studio Code.

    3.  In the **Extensions** menu, search for and install the following extensions from Microsoft:

        - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

    4.  Close VS Code.

    ## **1.7 Install pgAdmin**

    Throughout this workshop, you will use pgAdmin to run queries against your PostgreSQL database. pgAdmin is the leading Open Source management tool for Postgres.

    1.  Download pgAdmin from <https://www.pgadmin.org/download/>.

    2.  Run the installer using the default options.

=== "2. Fork repo"

    You must create a copy (known as a fork) of the **PostgreSQL Solution Accelerator: Build your own AI Copilot** GitHub repo and then clone that onto your local computer so you can work with its contents. After completing this step, you should have:
    
    - [X] Forked the **PostgreSQL Solution Accelerator: Build your own AI Copilot** repo to your personal GitHub profile
    - [X] Created a local clone of the repo
    - [X] Opened the cloned repo in Visual Studio Code

    ## 2.1 Fork Repo To Your Profile

    Forking in GitHub refers to creating a personal copy of a public repository, which allows you to freely experiment with changes without affecting the original project.

    1. To fork the repo, open a new browser window or tab and navigate to <https://github.com/solliancenet/microsoft-postgresql-solution-accelerator-build-your-own-ai-copilot>.

    2. Select the **Fork** button to create a copy of the repo in your GitHub profile.

        ![The Fork button is highlighted on the GitHub toolbar.](../../img/git-hub-toolbar-fork.png)

    3. Login with your GitHub profile, if prompted.

    3. On the **Create a new fork** page, select **Create fork** to make a copy of the repo under your GitHub profile.

        ![Screenshot of the Create a new fork page in GitHub.](../../img/github-create-fork.png)

    4. The forked repo will open within your GitHub profile.

    ## 2.2 Clone the Forked Repo

    1. On the GitHub page for your fork, select the **Code** button and then select the **Copy URL to clipboard** button next to the repo's HTTPS clone link:

        ![The GitHub Code menu is expanded and the copy button for the HTTPS clone link is highlighted.](../../img/github-code-clone-https.png)

    2. Open a new command prompt and change directories to the folder in which you want to clone the repo (e.g., D:\repos).

    3. Once in the desired directory, run the following `git clone` command to download a copy of your fork onto your local machine. Ensure you replace the `<url_of_your_forked_repo>` token with the clone link you copied in the previous step.

        ```bash title=""
        git clone <url_of_your_forked_repo>
        ```

    4. Once the repository has been cloned, change directories at the command prompt to the folder of the cloned repo, then run the following command to open the project in Visual Studio Code:

        ```bash title=""
        code .
        ```

    !!! tip "Leave Visual Studio Code open as you will be using it throughout the remainder of the workshop."

=== "3. Provision Azure infrastructure"

    This solution contains an Azure Developer CLI `azd-template` that provisions the required resources in Azure and deploys the starter app to Azure Container Apps (ACA). The template allows for the infrastructure to be deployed with a single `azd up` command. On completing this step, you should have:

    - [X] Selected an Azure region for workshop resources
    - [X] Verified your Azure ML CPU quota
    - [X] Authenticated with Azure
    - [X] Provisioned Azure resources and deployed the starter solution

    ## 3.1 Select an Azure region for your workshop resources

    To ensure you can successfully deploy the Azure resources using the `azd up` command, you must choose a region that supports the required Azure OpenAI `gpt-4o` and `text-embedding-3-large` models.

    1. Before deciding on the Azure region you want to use for your workshop resources, review the regional availability guidance for the [gpt-4o](https://learn.microsoft.com/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#standard-models-by-endpoint) and [text-embedding-3-large](https://learn.microsoft.com/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-embeddings#standard-models-by-endpoint) models in Azure OpenAI.
    
    2. Choose a region that **supports both models** and has quota available.

    !!! danger "Select a region that supports both models!"
    
        Choosing a region that doesn't support both models will result in deployment failure when running `azd up`.

    ## 3.2 Verify Azure ML CPU Quota

    This solution accelerator contains a section dedicted to setting up and using a Semantic Ranking model directly from your PostgreSQL database. The deployment of this component of the architecture requires sufficient CPU quota (32 cores) in Azure Machine Learning to accomodate the [Hugging Face BGE reranker model deployment](https://huggingface.co/BAAI/bge-reranker-v2-m3). In this task, you must verify you have available quota for the target virtual machine (VM) instance type (`STANDARD_D16AS_V4`), and if not, request additional quota.

    3. To view your available quota, you first need to retrieve your Microsoft Entra ID **Tenant ID** from the [Azure portal](https://portal.azure.com/).

    4. In the Azure portal, enter "Microsoft Entra ID" into the search bar, then select **Microsoft Entra ID** from the **Services** list in the results.

        ![Microsoft Entra ID is entered into the Azure search bar and it is highlighted in the Services results.](../../img/azure-portal-search-entra-id.png)

    5. On the **Overview** page of your Microsoft Entra ID tenant, select the **Copy to clipboard** button for your **Tenant ID**.

        ![On the Entra ID tenant overview tab, the copy to clipboard button for the Tenant ID is highlighted with a red box.](../../img/azure-portal-entra-id-tenant-overview.png)

    6. Open a new browser window or tab and navigate to the following URL, replacing the `<your-tenant-id>` token with the Tenant ID you copied from the Entra ID overview page in the Azure portal.

        ```bash title="Azure ML Quota page"
        https://ml.azure.com/quota?tid=<your-tenant-id>
        ```

    7. On the Azure ML **Quota** page, select the subscription you are using for this workshop.

        ![Screenshot of the Azure ML quota subscription selection page.](../../img/azure-ml-quota-subscription.png)

    8. On the quota page for your selected subscription, select the Azure region you plan to use for this workshop. This should be the region you chose in previous task that supports the required Azure OpenAI models.

    9. You should now see a list of CPUs and their quotas within your subscription. Locate **Standard DASv4 Family Cluster Dedicated vCPUs** in the list and inspect the **Quota** available.
        
        ![On the subscription quota page for the selected region, the Standard DASv4 Family Cluster Dedicated vCPUs items is highlighted and the available quota is highlighted.](../../img/azure-ml-quota-standard-dasv4.png)

    10. If you have 32 cores or more available, you can skip to the [Authenticate With Azure task](#33-authenticate-with-azure). Otherwise, select the **Standard DASv4 Family Cluster Dedicated vCPUs** by checking the box to the left of the name, then scroll up to the top of the page and locate the **Request quota** button.

        ![Screenshot of the Azure ML quota page with the Request quota button highlighted with a red box.](../../img/azure-ml-request-quota.png)

    11. In the **Request quota** dialog, increase your **New cores limit** value by 32 and then select **Submit**.

        ![Screenshot of the Request quota dialog with a value of 32 highlighted in the new cores limit box and the submit button highlighted.](../../img/azure-ml-request-quota-dialog.png)

        !!! example

            Your **new cores limit** should be increased to ensure 32 cores are available for a new deployment. For example, if you have zero cores available, your new cores limit should be set to 32. If your core limit is 100 and you are currently using 90, your new cores limit should be set to 122.

    12. Quota increase requests typically take a few minutes to complete. You will recieve notifications in the Azure portal as the request is processed and when it completes.

    13. If your request is denied, you don't have permissions to issue the request, or you prefer not to request additional quota, you have the option to exclude the **Semantic Ranking** model deployment when running the `azd up` command by setting the `deployAMLModel` flag to `false` when prompted.

    ## 3.3 Authenticate With Azure

    Before running the `azd up` command, you must authenticate your VS Code environment to Azure.
    
    1. To create Azure resources, you need to be authenticated from VS Code. Open a new intergated terminal in VS Code. Then, complete the following steps:
    
    !!! note "Step 1: Authenticate with `az` for post-provisioning tasks"
    
    2. Log into the Azure CLI `az` using the command below.
    
        ```bash  title=""
        az login
        ```

    3. Complete the login process in the browser window that opens.

        !!! info "If you have more than one Azure subscription, you may need to run `az account set -s <subscription-id> to specify the correct subscription to use."

    !!! note "Step 2: Authenticate with `azd` for provisioning & managing resources"
    
    4. Log in to Azure Developer CLI. This is only required once per-install.
    
        ```bash title=""
        azd auth login
        ```
    
    ## 3.4 Provision Azure Resource and Deploy App (UI and API)

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
              - **Enter a value for the `deployAMLModel`**: Select `True` if you were able to ensure you have sufficient Azure ML CPU quota avaiable to deploy the model. Otherwise, choose `False`.
                - If you select `False`, you will need to skip the optional **Semantic Ranker** section of this accelerator.
              - **Enter a value for the `postgresqlAdminPassword`**: Enter the password you want to use for the admin account on your Azure Database for PostgreSQL flexible server.
                - Ensure you copy the password in a secure location so you can use it later to access the database.
              - **Enter a value for the `resourceGroupName`**: Enter `rg-postgresql-accelerator`, or a similar name.

    2. Wait for the process to complete. It may take 30-45 minutes or more.

        !!! failure "Not enough subscription CPU quota"
    
            If you did not check your Azure ML CPU quota prior to starting running the `azd up` command, you may receive a CPU quota error message similar to the following:

            _(OutOfQuota) Not enough subscription CPU quota. The amount of CPU quota requested is 32 and your maximum amount of quota is [N/A]. Please see troubleshooting guide, available here: https://aka.ms/oe-tsg#error-outofquota_

            You can still continue with the workshop, but will need to skip the optional **Semantic Ranking** section, as you will not have the deployed model available.
 
    3. On successful completion you will see a `SUCCESS: ...` message on the console.

=== "4. Setup dev environment"

    In this step, you will configure your Python development environment in Visual Studio Code. At the end of this step, you should have:

    - [X] Created a Python virtual environment
    - [X] Installed the required Python libraries from `requirements.txt`
    - [X] Create and populated a `.env` file in the **Woodgrove API** project.
    - [X] Connected to your database using pgAdmin

    ## **4.1 Create a Python virtual environment**

    Virtual environments in Python are essential for maintaining a clean and organized development space, allowing individual projects to have their own set of dependencies, isolated from others. This prevents conflicts between different projects and ensures consistency in your development workflow. By using virtual environments, you can manage package versions easily, avoid dependency clashes, and keep your projects running smoothly. It's a best practice that keeps your coding environment stable and dependable, making your development process more efficient and less prone to issues.
    
    1. Return to Visual Studio Code, where you have the **PostgreSQL Solution Accelerator: Build your own AI Copilot** project open.
    
    2. In Visual Studio Code, open a new terminal window and change directories to the `src/api` folder of the repo.
    
    3. Create a virtual environment named `.venv` by running the following command at the terminal prompt:
    
        ```bash title=""
        python -m venv .venv 
        ```
    
        The above command will create a `.venv` folder under the `api` folder, which will provide a dedicated Python environment for the `api` project that can be used throughout this lab.
    
    4. Activate the virtual environment.

        !!! note "Select the appropriate command for your OS and shell from the table."
    
            | Platform | Shell | Command to activate virtual environment |
            | -------- | ----- | --------------------------------------- |
            | POSIX | bash/zsh | `source .venv/bin/activate` |
            | | fish | `source .venv/bin/activate.fish` |
            | | csh/tcsh | `source .venv/bin/activate.csh` |
            | | pwsh | `.venv/bin/Activate.ps1` |
            | Windows | cmd.exe | `.venv\Scripts\activate.bat` |
            | | PowerShell | `.venv\Scripts\Activate.ps1` |

    5. Execute the command at the terminal prompt to activate your virtual environment.
    
    ## **4.2 Install required Python libraries**
    
    The `requirements.txt` file in the `src\api` folder contains the set of Python libraries needed to run the Python components of the solution accelerator.

    !!! tip "Review required libraries"

        Open the `src\api\requirements.txt` file in the repo to review the required libraries and the versions that are being used.

    1. From the integrated terminal window in VS Code, run the following command to install the required libraries in your virtual environment:

        ```bash title=""
        pip install -r requirements.txt
        ```

    ## **4.3 Create `.env` file**

    Configuration values, such as connection string and endpoints, that allow your application to interact with Azure services are hosted in an Azure App Configuration service. To enable your application to retrieve these values, you must provide it with the endpoint of that service. You will use a `.env` file to host the endpoint as an environment variable, which will allow you to run the Woodgrove API locally. The `.env` file will be created within the `src\api\app` folder of the project.

    1. In VS Code, navigate to the `src\api\app` folder in the **Explorer** panel.

    2. Right-click the `app` folder and select **New file...** from the context menu.

    3. Enter `.env` as the name of the new file within the VS Code **Explorer** panel.

    4. In the `.env` file, add the following as the first line, replacing the `{YOUR_APP_CONFIG_ENDPOINT}` with the endpoint for the App Configuration resource in your `rg-postgresql-accelerator` resource group.

        ```ini title=""
        AZURE_APP_CONFIG_ENDPOINT={YOUR_APP_CONFIG_ENDPOINT}
        ```

        !!! note "Retrieve the endpoint for your App Configuration resource"

            To get the endpoint for your App Configuration resource:

            1. Navigate to your App Configuration resource in the [Azure portal](https://portal.azure.com/).
            
            2. Select **Access settings** from the resource navigation menu, under **Settings**.
            
            3. Copy the **Endpoint** value and paste it into the `.env` file.

                ![Screenshot of the App Configuration Access Settings page, with the Endpoint copy button highlighted.](../../img/app-config-access-settings-endpoint.png)

    5. Save the `.env` file.

    ## **4.4 Connect to your database from pgAdmin**

    You will use pgAdmin from your machine to configure various features in the database and execute queries to test those features. The `azd up` deployment script added your Microsoft Entra ID user as the owner of the database, so you will authenticate with Entra ID to. Please follow the steps below to connect to your Azure Database for PostgreSQL - Flexible Server using pgAdmin:

    1. Navigate to your Azure Database for PostgreSQL - Flexible Server resource in the [Azure portal](https://portal.azure.com/).

    2. On the Azure Database for PostgreSQL - Flexible Server page, copy the **Server name** value from the **Essentials** panel on the **Overview** page by selecting the _Copy to clipboard_ button to the right of the value.

        ![Screenshot of the Azure Database for PostgreSQL - Flexible Server Overview blade in the Azure portal, with the Server name highlighted.](../../img/azure-database-for-postgresql-server-name.png)

    3. On your development computer, open pgAdmin.

    4. In the pgAdmin **Object Explorer**, right-click on **Servers** and in the context menu select **Register >**, then **Server...**.

        ![Screenshot of the pgAdmin Servers context menu, with Register > Server highlighted.](../../img/pgadmin-register-server.png)

    5. In tab of **Register - Server** dialog, follow these steps:

        1. On the **General** tab, enter "PostgreSQLSolutionAccelerator" into the **Name** field and clear the **Connect now** option.

            ![Screenshot of the Register Server general tabl with the name and connect now fields highlighted.](../../img/pgadmin-register-server-general-tab.png)

        2. Select the **Connection** tab and provide your Azure Database for PostgreSQL flexible server instance details for **Hostname/address** and **Username**.

           1. Paste the **Server name** value of your Azure Database for PostgreSQL flexible server into the **Host name/address** field.

           2. The **Username** value is your Microsoft Entra ID or email.

        3. Select **Save**.

        4. Right-click the newly added **PostgreSQLSolutionAccelerator** server in the pgAdmin Object Explorer, and select **Connect Server** in the context menu.

            ![Screenshot of the server context menu, with Connect Server highlighted.](../../img/pgadmin-connect-server.png)

        5. In the **Connect to Server** dialog, you will need to provide an access token.

            !!! note "To Retrieve Your Microsoft Entra ID Access Token"

                1. In VS Code, open a new integrated terminal.

                2. At the integrated terminal prompt, execute the following command:

                    ```bash
                    az account get-access-token --resource-type oss-rdbms
                    ```

                    After authentication is successful, Microsoft Entra ID returns an access token:

                    ```json
                    {
                      "accessToken": "TOKEN",
                      "expiresOn": "...",
                      "subscription": "...",
                      "tenant": "...",
                      "tokenType": "Bearer"
                    }
                    ```

                3. Copy the `TOKEN` value in the `accessToken` property (without the surrounding quotes).

                    !!! info "The token is a Base64 string. It encodes all the information about the authenticated user and is targeted to the Azure Database for PostgreSQL service."

        6. Return to pgAdmin and the **Connect to Server** dialog and paste the access token into the password field.

            ![Screenshot of the Connect to Server dialog, with the access token entered into the password box.](../../img/pgadmin-connect-to-server.png)

        7. Select **OK**.

            !!! warning "Access token expiration"

                Your access token will be good for an hour, so you may need to come back and repeat the above steps multiple times throughout the course of the workshop.

    !!! tip "Leave pgAdmin open as you will be using it throughout the remainder of the workshop."

    ---

    ## Next → [Validate Setup](./03-Validation.md)
