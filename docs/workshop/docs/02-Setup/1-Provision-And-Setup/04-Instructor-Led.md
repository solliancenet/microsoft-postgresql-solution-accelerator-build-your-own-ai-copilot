# B. Instructor-Led Workshop Setup

Welcome to the Instructor-Guided Lab Track! You will need a valid Azure subscription, a GitHub account, and access to relevant Azure OpenAI models to complete this lab. Review the [prerequisites](../../0-Prerequisites/#instructor-led-workshop) section if you need more details.

!!! question "WERE YOU LOOKING FOR THE SELF-GUIDED OPTION INSTEAD? [You can find that here.](./03-Self-Guided.md)"

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

1. Navigate to the `./workshop` folder within the cloned repo.

    ```bash title=""
    cd workshop
    ```

    The `./workshop` folder contains the Instructor-Led version of the infrastructure and Azure Developer CLI templates.

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

3. Wait for the process to complete. It may take 30-45 minutes or more.

    !!! failure "Not enough subscription CPU quota"

        If you did not check your Azure ML CPU quota prior to starting running the `azd up` command, you may receive a CPU quota error message similar to the following:

        _(OutOfQuota) Not enough subscription CPU quota. The amount of CPU quota requested is 32 and your maximum amount of quota is [N/A]. Please see troubleshooting guide, available here: https://aka.ms/oe-tsg#error-outofquota_

        You can still continue with the workshop, but will need to skip the optional **Semantic Ranking** section, as you will not have the deployed model available.

4. On successful completion you will see a `SUCCESS: ...` message on the console.

!!! tip "When following the Instructor-Led version of this guide, it is required to run all `azd up` and `azd deploy` commands from within the `./workshop` folder."

## Deploy Azure OpenAI Models

Now that the infrastructure has been provisioned, you are now ready to deploy the completions and embeddings models to Azure OpenAI Service. These models will be used when implementing the AI integration into the application. On completing this step, you will have these models deployed:

- [X] **Completions**: The `gpt-40` model will be used for chat completions for the Copilot implementation.
- [X] **Embeddings**: The `text-embedding-ada-002` model will be used to generate text embeddings that will be used to implement vector search for the Copilot implementation.

Follow these steps to deploy the Azure OpenAI models:

1. Open a new browser tab to navigate to the link below. You may be prompted to login.

    ```text title=""
    https://portal.azure.com/#browse/resourcegroups
    ```

2. You may be presented with a "Welcome ot Microsoft Azure" screen. Select **Cancel** (to dismiss it) or click **Get Started** (to take an introductory tour of the Azure Portal).

3. You should be taken directly to the Resource Groups page for your subscription. In the list of resource groups, locate the one named `rg-postgresql-accelerator` (or, if you assigned a different name, find that one). This resource group was created for you as part of the `azd up` resource deployment. It contains all of the Azure resources required to build and deploy your AI-enabled solution.

    !!! tip "You can use the search filter to reduce the number resource groups displayed."

4. Select your resource group.

5. Within the list of resources within the resource group, locate and select the **Azure OpenAI** resource.

    ![Screenshot of resources in the resource group, with Azure OpenAI service highlighted.](../../img/azure-openai-resource-list.png)

6. In the **Get Started** section of the Azure OpenAI resources **Overview** page, select the **Explore Azure AI Foundry portal** button to open up the Azure AI Foundry. You might be prompted to login the the AI Foundry.

    ![Screenshot of the Azure OpenAI resource, with the Explore Azure AI Foundry portal button highlighted.](../../img/azure-openai-resource-ai-foundry-portal-button.png)

7. In the Azure AI Foundry, select the **Deployments** option in the left-side navigation.

    ![Screenshot of the Azure AI Foundry with the Deployments navigation option highlighted.](../../img/azure-ai-foundry-deployments-option.png)

8. On the **Model deployments** page, select the **Deploy model** button, then select the **Deploy base model** option.

    ![Screenshot of the Model deployments page with the Deploy model button and Deploy base model option highlighted.](../../img/azure-ai-foundry-deployments-deploy-base-model-button.png)

9. On the **Select a model** dialog, select the **gpt-4o** model, then select **Confirm**.

    ![Screenshot of the Select a model dialog with gpt-4o model highlighted.](../../img/azure-ai-foundry-select-model-gpt4o.png)

10. On the **Deploy model gpt-4o** dialog, ensure that `completions` is entered in the **Deployment name** field, then select **Deploy**. This will deploy the OpenAI GPT-4o completions model to the Azure OpenAI service. The name of the deployment must be `completions` for this workshop since the application code depends on this name.

    ![Screenshot of Deploy model gpt-4o dialog with deployment name entered.](../../img/azure-ai-foundry-deploy-model-gpt4o.png)

11. Next, you'll deploy the Embeddings model. In the Azure AI Foundry, select the **Deployments** option in the left-side navigation.

    ![Screenshot of the Azure AI Foundry with the Deployments navigation option highlighted.](../../img/azure-ai-foundry-deployments-option.png)

12. On the **Model deployments** page, select the **Deploy model** button, then select the **Deploy base model** option.

13. On the **Select a model** dialog, select the **text-embedding-ada-002** model, then select **Confirm**.

    ![Screenshot of the Select a model dialog with the text-embedding-ada-002 model highlighted.](../../img/azure-ai-foundry-select-model-text-embedding-ada-002.png)

14. On the **Deploy model gpt-4o** dialog, ensure that `embeddings` is entered in the **Deployment name** field, then select **Deploy**. This will deploy the OpenAI GPT-4o completions model to the Azure OpenAI service. The name of the deployment must be `embeddings` for this workshop since the application code depends on this name.

    ![Screenshot of Deploy model text-embedding-ada-002 dialog with deployment name entered.](../../img/azure-ai-foundry-deploy-model-text-embedding-ada-002.png)

15. You can successfully deployed the `gpt-4o` model that will be used for chat completions, and the `text-embedding-ada-002` model that will be used to generate text embeddings.


<!--
We use the [Skillable VM](https://skillable.com) - a _lab-on-demand_ platform with a built-in Azure subscription and pre-provisioned resources - to give you a fast start.

!!! question "WERE YOU LOOKING FOR THE SELF-GUIDED OPTION INSTEAD? [You can find that here.](./03-Self-Guided.md)"

---

## 1. Launch Skillable VM

To continue with Skillable-based Setup, you will need the **Lab Launch URL** (link or QR Code) given to you by your instructor at the start of the session. On completing this step, you should have:

- [X] The Skillable VM tab open, with the Azure subscription details shown.
- [X] The Skillable countdown timer visible, with _at least 1h 15 mins_ remaining.
- [X] The `Deploy` button clicked, and showing a _Successful_ completion message.
- [X] This instruction guide open, with this section in focus.

**If you already completed these steps in-venue with instructor help, then skip ahead to [Step 2](#2-launch-github-codespaces)**. Otherwise, expand the section below to complete the task now.

??? note "GET STARTED: Launch Skillable VM, Click Deploy Button, Open Workshop Guide"

    The lab instructor should have shared a Skillable Lab link (URL or QR Code).

    - Open the browser and navigate to the link - _locate LAB401 in the page_.
    - Click the **Launch** button - _wait till the launched page completes loading_.
        - (Left) You will see a login screen - _we can ignore this for now_
        - (Top Right) You will see a countdown timer - it should start at 1hr 15 mins. 
        - (Below that) You will see a **Deploy** button - we will use this, next.
        - (Below That) You should see the instructions panel - we'll validate this, after.
    - Click the **Deploy** button - _wait till the loading progress icon stops_.
        - This triggers a background task to deploy our application to Azure
        - **This step can take a few minutes to complete**
        - When done, you should see a "Success" dialog below the button.
        - *Note: The dialog may use a red background to alert you - this does not imply failure!*
    - Review other **Instructions Panel** details:
        - Check the lab title - should be _Build a Retail Copilot Code-First on Azure AI_
        - Check the Azure subscription - should have _username & password_ details filled in
        - Check the Workshop guide link - should open to a hosted version of this guide.
     
    **Leave the Skillable tab open in your browser**. We'll use the Azure credentials in the next step. And we'll revisit this tab at the end, to complete lab teardown. You can also track remaining lab time in the countdown timer.

---

## 2. Launch GitHub Codespaces

The Contoso Chat sample repository is instrumented with a [dev container](https://containers.dev) which specifies required tools and dependencies. Simply launch this from GitHub Codespaces to get a pre-built development environment with a Visual Studio Code editor and Python runtime ready to go.

At the end of this step you should have:

- [X] Launched GitHub Codespaces to get the pre-built dev environment.
- [X] Forked the sample repo to your personal GitHub profile.
- [X] Verified that required command-line tools were installed.

### 2.1 Navigate to GitHub & Login


1. Open a browser tab (T1) and navigate to the link below.

    !!! tip "In codeblocks like this, click the icon (far right) to copy text to clipboard!"

    ``` title=""
    https://aka.ms/contoso-chat/prebuild
    ```

1. You will be prompted to log into GitHub. **Login now with your GitHub profile.**

### 2.2 Setup GitHub Codespaces

1. You will see a page titled **"Create codespace for Azure-Samples/contoso-chat"**
    - Check branch is `msignite-LAB401` 
    - Check dev container config is `Contoso Chat (v2)` and region is `US East`
    - Click dropdown for **2-core** and verify it is `Prebuild ready`

    !!! tip "Using the pre-build option makes your GitHub Codespaces load up faster."

1. Click the green "Create codespace" button
    - You should see a new browser tab open to a link ending in `*.github.dev`
    - You should see a Visual Studio Code editor view loading (takes a few mins)
    - When ready, you should see the README for the "Contoso Chat" repository
    
    !!! warning "The README is for information only. Please continue to follow _this_ guide for the workshop."

### 2.3 Fork Repo To Your Profile

Your GitHub Codespaces is running on the _original_ Azure Samples repo for this sample. Let's fork this now, so we have a personal copy to modify and reviist. We will use the GitHub CLI to complete this in just a few quick steps!


1. Open the VS Code terminal and run this command to verify the GitHub CLI is installed.

    ```bash title=""
    gh --version
    ```
    
1. Next, run this command to authenticate with GitHub, with scope set to allow fork actions.

    ```bash title=""
    GITHUB_TOKEN="" gh auth login --hostname github.com --git-protocol https --web --scopes workflow 
    ```

    The command ensures we complete the auth workflow from the web browser using the Git protocol over a secure HTTPS connection, and scope limited to workflow actions. Using an empty GITHUB_TOKEN ensure we don't use an existing token with broader scope.

1. Follow the prompts to complete auth flow. (Expand the sections below for an example)

    ??? note "1. Complete Device Activation flow"

        - Say "Yes" when prompted to authenticate with GitHub credentials
        - Copy the one-time code provided in the console
        - Press "Enter" to open the Device Activation window
        - Copy the code into that window as shown below

            Here is an example of what that looks like:

            ![Activation](./../../img/gh-cli-activation.png)

    ??? note "2. Confirm GitHub authorization scope"

        - You should see this authorization dialog on activation
        - Click the green "Authorize github" button to continue
        - This gives the GitHub CLI (this session) permission to do the fork

            ![Activation](./../../img/gh-cli-confirmation'.png)

    ??? note "3. Verify you are Logged in."

        - The console log should show you are logged in successfully

            ![Activation](./../../img//gh-cli-authflow.png)

1. Now, run this command to fork the repo.

    ``` title=""
    GITHUB_TOKEN="" gh repo fork --remote
    ```

    You should see a `Created fork..` followed by an `Added remote origin ..` message. On completion, you should have a fork of the repo in your personal profile _and_ your local Codespaces environment will now be setup to commit changes to your fork.

1. **Optional**. Visit your GitHub profile and check that the fork was created. It should be at the location in the form `https://github.com/<username>/contoso-chat` where `<username>` should be replaces by your GitHub profile.

### 2.4 Check Tools Installed

The workshop uses the following tools and commands: `python`, `fastapi`, `prompty`, `az`, `azd`. These are pre-installed for you, but you can optionally verify these to get a sense for their current versions.

??? note "(Optional: Expand to view details) Verify intalled tools." 

    ```bash title=""
    python --version
    ```
    ```bash title=""
    fastapi --version
    ```
    ```bash title=""
    prompty --version
    ```
    ```bash title=""
    az version
    ```
    ```bash title=""
    azd version
    ```


## 3. Authenticate with Azure

To access our Azure resources, we need to be authenticated from VS Code. Make sure the Terminal pane is active in the GitHub Codespaces tab. Then, complete both the steps below (click each to expland for instructions).

??? note "1. Authenticate with `az` for post-provisioning tasks"

    1. Log into the Azure CLI `az` using the command below. 

        ``` title=""
        az login --use-device-code
        ```

    1. Copy the 8-character code shown to your clipboard, then control-click the link to visit [https://microsoft.com/devicelogin](https://microsoft.com/devicelogin) in a new browser tab.

    1. Select the account with the Username shown in the Skillable Lab window. Click "Continue" at the `are you sure?` prompt, and then close the tab

    1. Back in the Terminal, press Enter to select the default presented subscription and tenant.


??? note "2. Authenticate with `azd` for provisioning & managing resources"

    1. Log into the Azure Developer CLI using the command below. 

        ``` title=""
        azd auth login --use-device-code
        ```

    1. Follow the same process as before - copy code, paste it when prompted, select account.
    1. Note: you won't need to enter the password again. Just select the Skillable lab account.

!!! success "CONGRATULATIONS. You are logged in from Azure CLI and Azure Developer CLI"

## 4. Configure Env Variables

To build code-first solutions, we will need to use the Azure SDK from our development environment. This requires configuration information for the various resources we've already provisioned for you in the `francecentral` region. Let's retrieve those now.

1. Run the commands below in the same Visual Studio Code terminal.

    ``` title=""
    azd env set AZURE_LOCATION francecentral -e AITOUR --no-prompt
    ```
    ``` title=""
    azd env refresh -e AITOUR 
    ```

    (Press ENTER to select the default Azure subscription presented). 

2. Verify the environment variables were refreshed.

    The above commands will have created a `.azure/AITOUR/.env` file in your GitHub Codespaces environment with all the configuration information we will need to build our app. You can open the file from the VS Code file explorer **or** you can run the command below to view the values in the terminal:

    ``` title=""
    azd env get-values
    ```

    !!! tip "Note that the `.env` file does not contain any secrets (passwords or keys). Instead, we use  [Azure Managed Identities](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview) for keyless authentication as a _security best practice_" 


## 5. Do Post-Provisioning

_We can now use these configured tools and SDK to perform some post-provisioning tasks. This includes populating data in Azure AI Search (product indexes) and Azure Cosmos DB (customer data), and deploying the initial version of our application to Azure Container Apps_.

Return to the Visual Studio Code Terminal above:

1. Run the command below. (This will take a few minutes to complete.)

    ``` title=""
    bash ./docs/workshop/src/0-setup/azd-update-roles.sh
    ```

    !!! info "We pre-provisioned the Azure resources for you using a service principal. In this step, we update the resource roles to allow user access so you can populate data in Azure AI Search and Azure Cosmos DB from code. This step is not required in self-guided mode where you provision all resources yourself."

1. Once complete, run the command below. It will take a few minutes to complete.

    ``` title=""
    azd hooks run postprovision
    ```

    !!! info "This step runs the Jupyter Notebooks found in the relevant `data/` subfolders, populating the Azure AI Search and Azure CosmosDB resources with product catalog (index) and customer profile (orders)."
This step should take just a few minutes to complete from the commandline.

---

!!! success "CONGRATULATIONS. Your Skillable-based Setup is Complete! We'll Validate this, next!"

-->
