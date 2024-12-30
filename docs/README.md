---
page_type: sample
languages:
- azdeveloper
- python
- bash
- bicep
- prompty
products:
- azure
- azure-openai
- azure-cognitive-search
- azure-cosmos-db
urlFragment: contoso-chat
name: PostgreSQL Solution Accelerator - Build your own AI Copilot / FSI Scenario (Python Implementation)
description: Build, evaluate, and deploy, a RAG-based retail copilot that responds to customer questions with responses grounded in the retailer's product and customer data.
---
<!-- YAML front-matter schema: https://review.learn.microsoft.com/help/contribute/samples/process/onboarding?branch=main#supported-metadata-fields-for-readmemd -->

# PostgreSQL Solution Accelerator - Build your own AI Copilot / FSI Scenario

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://github.com/codespaces/new?hide_repo_select=true&machine=basicLinux32gb&repo=725257907&ref=main&devcontainer_path=.devcontainer%2Fdevcontainer.json&geo=UsEast)

## Table of Contents

- [PostgreSQL Solution Accelerator - Build your own AI Copilot / FSI Scenario](#postgresql-solution-accelerator---build-your-own-ai-copilot--fsi-scenario)
  - [Table of Contents](#table-of-contents)
  - [Important Security Notice](#important-security-notice)
  - [Overview](#overview)
  - [Pre-requisites](#pre-requisites)
  - [Getting Started](#getting-started)
    - [GitHub Codespaces](#github-codespaces)
    - [Local environment](#local-environment)
  - [Development](#development)
  - [Testing](#testing)
  - [Deployment](#deployment)
  - [Guidance](#guidance)
    - [Region Availability](#region-availability)
    - [Costs](#costs)
    - [Security](#security)
  - [Workshop](#workshop)
    - [Lab Guide](#lab-guide)
  - [Resources](#resources)
  - [Code of Conduct](#code-of-conduct)
  - [Responsible AI Guidelines](#responsible-ai-guidelines)

## Important Security Notice

This template, the application code and configuration it contains, has been built to showcase Microsoft Azure specific services and tools. We strongly advise our customers not to make this code part of their production environments without implementing or enabling additional security features.  

For a more comprehensive list of best practices and security recommendations for Intelligent Applications, visit our [official documentation](https://learn.microsoft.com/azure/developer/ai/get-started-securing-your-ai-app).

**Sample application code is included in this project**. You can use or modify this app code or you can rip it out and include your own.

<br/>

## Overview

In the financial services industry, validating contracts, statements of work (SOWs), and invoices poses distinct challenges. This is particularly true when it comes to ensuring that invoices align with SOWs, especially for milestone-based payments and other specific deliverables. Traditionally, this validation process is manual, requiring meticulous comparison and cross-checking, often leading to delays, errors, and elevated operational costs. This accelerator explores a high-level architectural solution utilizing Microsoft Azure's comprehensive suite of services to automate and streamline this process, resulting in faster, more accurate, and cost-effective invoice validation.

The objective of this solution is to automate the extraction, validation, and storage of invoices and SOWs to minimize manual effort and boost operational efficiency. This solution architecture facilitates seamless integration across multiple Azure services, ensuring scalability, security, and optimized costs, while accurately aligning invoices with milestone-based deliverables and other contractual obligations.

The high-level solution architecture is represented by this diagram:

![High-level architecture diagram for the solution](../docs/workshop/docs/img/solution-architecture-diagram.png)

**High-Level Workflow**:

1. **Data Ingestion**: SOWs, invoices and other related documents are ingested via a custom REACT web application. Internal users and external vendors can submit documents by uploading them through the web app, which then uploads them to Azure Blob Storage.

2. **Workflow Trigger Mechanism**: Upon receipt of new documents, an event trigger activates Python-based background worker processes:

   a. **Data Extraction and Processing**: Azure's OCR (Optical Character Recognition) technology digitizes content from uploaded documents, such as SOWs and invoices.

   b. **Document Intelligence (Custom Model)**: A custom AI model within Azure's Document Intelligence service is tailored to extract specific data fields, like payment milestones, dates, amounts, and vendor details. This model is trained to recognize the structure of financial documents, improving data extraction accuracy.

   c. **Confidence Scoring and Validation**: Each document is assigned a confidence score based on whether the documents contain the correct sections and fields.

   d. **Validation Using Azure OpenAI**: Azure OpenAI language models, such as GPT-4o, are used to review all document data, employing natural language understanding to validate and cross-check information, ensuring high data integrity. The language model is used to cross-reference data between invoices and SOWs, evaluating payment milestone completion and billing, and preventing issues like payment delays. It also validates that appropriate compliance language exists in contracts and SOWs, helping to avoid compliance violations.

3. **Secure Storage and Database Management**: Validated data is chunked, vectorized using an Azure OpenAI embedding model, and stored in an encrypted Azure Database for PostgreSQL flexible server database, which uses vector embeddings for advanced search and retrieval. This supports efficient handling of structured and semi-structured data, facilitating downstream analytics. Azure Database for PostgreSQL flexible server supports JSON-based semi-structured data and vector embedding storage, enabling AI-enhanced queries. Embeddings can be generated directly from database queries using the Azure AI extension for PostgreSQL.

4. **Document enrichment**: The Azure AI extension for PostreSQL also enables data to be enhanced using Azure AI Services directly from the database. This capability provides rich AI functionality, such as text translation and entity and keyword extraction.

5. **Copilot chat**: An Azure OpenAI + LangChain copilot enables project managers and leadership to quickly get metrics, trends and processing timelines for contracts, SOWs, invoices, and vendors using a user friendly chat interface. Function calling via LangChain tools enables the copilot to implement a RAG (retrieval-augmented generation) pattern over data in the PostgreSQL database, using vector search to efficiently retrieve relevant documents and data.

This diagram highlights a comprehensive workflow for handling document processing and data enrichment using Azure services, integrating AI and machine learning capabilities with PostgreSQL for efficient data management and storage.

## Pre-requisites

To deploy and explore the sample, you will need:

1. An active Azure subscription - [Signup for a free account here](https://azure.microsoft.com/free/)
1. An active GitHub account - [Signup for a free account here](https://github.com/signup)
1. Access to Azure OpenAI Services - [Learn about Limited Access here](https://learn.microsoft.com/legal/cognitive-services/openai/limited-access)
1. Access to Azure AI Search - [With Semantic Ranker](https://learn.microsoft.com/azure/search/semantic-search-overview) (premiun feature)
1. Available Quota for: `text-embedding-ada-002`, `gpt-35-turbo`. and `gpt-4`

We recommend deployments to `swedencentral` or `francecentral` as regions that can support all these models. In addition to the above, you will also need the ability to:

- provision Azure Monitor (free tier)
- provision Azure Container Apps (free tier)
- provision Azure CosmosDB for noSQL (free tier)

From a tooling perspective, familiarity with the following is useful:

- Visual Studio Code (and extensions)
- GitHub Codespaces and dev containers
- Python and Jupyter Notebooks
- Azure CLI, Azure Developer CLI and commandline usage

## Getting Started

You have two options for setting up your development environment:

1. Use GitHub Codespaces - for a prebuilt dev environment in the cloud
2. Use Manual Setup - for control over all aspects of local env setup

**We recommend going with GitHub Codespaces** for the fastest start and lowest maintenance overheads. Pick one option below - click to expand the section and view the details.

### GitHub Codespaces

1. You can run this template virtually by using GitHub Codespaces. Click this button to open a web-based VS Code instance in your browser:

    [![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://github.com/codespaces/new?hide_repo_select=true&machine=basicLinux32gb&repo=725257907&ref=main&devcontainer_path=.devcontainer%2Fdevcontainer.json&geo=UsEast)

1. Once the codespaces environment is ready (this can take several minutes), open a new terminal in that VS Code instance - and proceed to the [Development](#development) step.

### Local environment

1. **Install the required tools** in your local device:
    - [Azure Developer CLI (azd)](https://aka.ms/install-azd)
    - [Python 3.10+](https://www.python.org/downloads/)
    - [Docker Desktop](https://www.docker.com/products/docker-desktop/)
    - [Git](https://git-scm.com/downloads)

    **Note for Windows users:** If you are _not_ using a container to run this sample, note that our post-provisioning hooks make use of shell scripts. While we update scripts for different local device environments, we recommend using [git bash](https://gitforwindows.org/) to run samples correctly.

1. **Initialize the project** in your local device:

    TODO: Add steps

1. **Install dependencies** for the project, manually.

    ```bash
        cd src/api
        pip install -r requirements.txt
    ```

You can now proceed to the next step - [Development](#development) - where we will provision the required Azure infrastructure and deploy the application from the template using `azd`.

## Development

Once you've completed the setup the project (using [Codespaces](#github-codespaces) or [local environment](#local-environment)) you should now have a Visual Studio Code editor open, with the project files loaded, and a terminal open for running commands. Let's verify that all required tools are installed.

```bash
az version
azd version
prompty --version
python --version
```

We can now proceed with next steps - click to expand for detailed instructions.

<details>
<summary> 1️⃣ | Authenticate With Azure </summary>

1. Open a VS Code terminal and authenticate with Azure CLI. Use the `--use-device-code` option if authenticating from GitHub Codespaces. Complete the auth workflow as guided.

    ```bash
    az login --use-device-code
    ```

1. Now authenticate with Azure Developer CLI in the same terminal. Complete the auth workflow as guided. 

    ```bash
    azd auth login --use-device-code
    ```

1. You should see: **Logged in on Azure.** This will create a folder under `.azure/` in your project to store the configuration for this deployment. You may have multiple azd environments if desired.

</details>

<details>
<summary> 2️⃣ |  Provision-Deploy with AZD </summary>

1. Run `azd up` to provision infrastructure _and_ deploy the application, with one command. (You can also use `azd provision`, `azd deploy` separately if needed)

    ```bash
    azd up
    ```

1. You will be asked for  a _subscription_ for provisioning resources, an _environment name_ that maps to the resource group, and a _location_ for deployment. Refer to the [Region Availability](#region-availability) guidance to select the region that has the desired models and quota available.
1. The `azd up` command can take 15-20 minutes to complete. Successful completion sees a **`SUCCESS: ...`** messages posted to the console. We can now validate the outcomes.
</details>

<details>
<summary> 3️⃣ | Validate the Infrastructure </summary>

1. Visit the [Azure Portal](https://portal.azure.con) - look for the `rg-ENVNAME` resource group created above
1. Click the `Deployments` link in the **Essentials** section - wait till all are completed.
<!-- 1. Return to `Overview` page - you should see: **35** deployments, **15** resources
1. Click on the `Azure CosmosDB resource` in the list
    - Visit the resource detail page - click "Data Explorer"
    - Verify that it has created a `customers` database with data items in it
1. Click on the `Azure AI Search` resource in the list
    - Visit the resource detail page - click "Search Explorer"
    - Verify that it has created a `contoso-products` index with data items in it
1. Click on the `Azure Container Apps` resource in the list
    - Visit the resource detail page - click `Application Url`
    - Verify that you see a hosted endpoint with a `Hello World` message on page
1. Next, visit the [Azure AI Studio](https://ai.azure.com) portal
    - Sign in - you should be auto-logged in with existing Azure credential
    - Click on `All Resources` - you should see an `AIServices` and `Hub` resources
    - Click the hub resource - you should see an `AI Project` resource listed
    - Click the project resource - look at Deployments page to verify models
1. ✅ | **Congratulations!** - Your Azure project infrastructure is ready! -->
</details>


<details>
<summary> 4️⃣ | Validate the Deployment </summary>

1. The `azd up` process also deploys the application as an Azure Container App or Azure Kubernetes Service
<!-- 1. Visit the ACA resource page - click on `Application Url` to view endpoint
1. Add a `/docs` suffix to default deployed path - to get a Swagger API test page
1. Click `Try it out` to unlock inputs - you see `question`, `customer_id`, `chat_history`
    - Enter `question` = "Tell me about the waterproof tents"
    - Enter `customer_id` = 2
    - Enter `chat_history` = []
    - Click **Execute** to see results: _You should see a valid response with a list of matching tents from the product catalog with additional details_.
1. ✅ | **Congratulations!** - Your Chat AI Deployment is working! -->

</details>

## Testing

We can think about two levels of testing - _manual_ validation and _automated_ evaluation. The first is interactive, exploring the deployed prototype as we iterate. The second is code-driven...
<!-- , using a test prompt dataset to assess quality and safety of prototype responses for a diverse set of prompt inputs - and score them for criteria like _coherence_, _fluency_, _relevance_ and _groundedness_ based on built-in or custom evaluators. -->

<details>
<summary> 1️⃣ | Manual Testing (interactive) </summary>
<br/>

<!-- The Contoso Chat application is implemented as a _FastAPI_ application that can be deployed to a hosted endpoint in Azure Container Apps. The API implementation is defined in `src/api/main.py` and currently exposes 2 routes:
 - `/` - which shows the default "Hello World" message
 - `/api/create_request` - which is our chat AI endpoint for test prompts

To test locally, we run the FastAPI dev server, then use the Swagger endpoint at the `/docs` route to test the locally-served endpoint in the same way we tested the deployed version/

- Change to the root folder of the repository
- Run `fastapi dev ./src/api/main.py` - it should launch a dev server
- Click `Open in browser` to preview the dev server page in a new tab
    - You should see: "Hello, World" with route at `/`
- Add `/docs` to the end of the path URL in the browser tab
    - You should see: "FASTAPI" page with 2 routes listed
    - Click the `POST` route then click `Try it out` to unlock inputs
- Try a test input
    - Enter `question` = "Tell me about the waterproof tents"
    - Enter `customer_id` = 2
    - Enter `chat_history` = []
    - Click **Execute** to see results: _You should see a valid response with a list of matching tents from the product catalog with additional details_.
1. ✅ | **Congratulations!** - You successfully tested the app locally -->

</details>

<details>
<summary> 2️⃣ | AI-Assisted Evaluation (code-driven) </summary>
<br/>

<!-- Testing a single prompt is good for rapid prototyping and ideation. But once we have our application designed, we want to validate the _quality and safety_ of responses against diverse test prompts. The sample shows you how to do **AI-Assisted Evaluation** using custom evaluators implemented with Prompty.

- Visit the `src/api/evaluators/` folder
- Open the `evaluate-chat-flow.ipynb` notebook - "Select Kernel" to activate
- Clear inputs and then `Run all` - starts evaluaton flow with `data.jsonl` test dataset
- Once evaluation completes (takes 10+ minutes), you should see
    - `results.jsonl` = the chat model's responses to test inputs
    - `evaluated_results.jsonl` = the evaluation model's scoring of the responses
    - tabular results = coherence, fluency, relevance, groundedness scores

Want to get a better understanding of how custom evaluators work? Check out the `src/api/evaluators/custom_evals` folder and explore the relevant Prompty assets and their template instructions.

The Prompty tooling also has support for built-in _tracing_ for observability. Look for a `.runs/` subfolder to be created during the evaluation run, with `.tracy` files containing the trace data. Click one of them to get a _trace-view_ display in Visual Studio Code to help you drill down or debug the interaction flow. _This is a new feature so look for more updates in usage soon_. -->

</details>

## Deployment

The solution is deployed using the Azure Developer CLI. The `azd up` command effectively calls `azd provision` and then `azd deploy` - allowing you to provision infrastructure and deploy the application with a single command. Subsequent calls to `azd up` (e.g., ,after making changes to the application) should be faster, re-deploying the application and updating infrastructure provisioning only if required. You can then test the deployed endpoint as described earlier.

## Guidance

### Region Availability

This template currently uses the following models: `gpt35-turbo`, `gpt-4` and `text-embedding-ada-002`, which may not be available in all Azure regions, or may lack sufficient quota for your subscription in supported regions. Check for [up-to-date region availability](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#standard-deployment-model-availability) and select a region during deployment accordingly

**We recommend using `francecentral`**

### Costs

Pricing for services may vary by region and usage and exact costs are hard to determine. You can _estimate_ the cost of this project's architecture with [Azure's pricing calculator](https://azure.microsoft.com/pricing/calculator/) with these services:

- Azure OpenAI - Standard tier, GPT-35-turbo and Ada models. [See Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
- Azure AI Search - Basic tier, Semantic Ranker enabled. [See Pricing](https://azure.microsoft.com/pricing/details/search/)
- Azure Database for PostgreSQL - Burstable Tier. [See Pricing](https://azure.microsoft.com/pricing/details/postgresql/flexible-server/#pricing)
- Azure Monitor - Serverless, Free Tier. [See Pricing](https://azure.microsoft.com/pricing/details/monitor/)
- Azure Container Apps - Severless, Free Tier. [See Pricing](https://azure.microsoft.com/pricing/details/container-apps/)

### Security

This template uses [Managed Identity](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview) for authentication with key Azure services including Azure OpenAI, Azure AI Search, and Azure Database for PostgreSQL. Applications can use managed identities to obtain Microsoft Entra tokens without having to manage any credentials. This also removes the need for developers to manage these credentials themselves and reduces their complexity.

Additionally, we have added a [GitHub Action tool](https://github.com/microsoft/security-devops-action) that scans the infrastructure-as-code files and generates a report containing any detected issues. To ensure best practices we recommend anyone creating solutions based on our templates ensure that the [Github secret scanning](https://docs.github.com/code-security/secret-scanning/about-secret-scanning) setting is enabled in your repo.

<br/>

## Workshop

The sample has a `docs/workshop` folder with step-by-step guidance for developers, to help you deconstruct the codebase, and understand how to to provision, ideate, build, evaluate, and deploy, the application yourself, with your own data.

### Lab Guide

1. [View Workshop Online](https://solliancenet.github.io/microsoft-postgresql-solution-accelerator-build-your-own-ai-copilot) - view a pre-built workshop version in your browser
1. **View Workshop Locally** - The workshop is built using Mkdocs. To preview it locally, 
    - install mkdocs: `pip install mkdocs-material`
    - switch to folder: `cd docs/workshop`
    - launch preview: `mkdocs serve`
    - open browser to the preview URL specified
    - (optional) deploy to GitHub Pages: `mkdocs gh-deploy`

Have issues or questions about the workshop? Submit [a new issue](https://github.com/solliancenet/microsoft-postgresql-solution-accelerator-build-your-own-ai-copilot/issues/new) with a `documentation` tag.

## Resources

1. [Azure AI Foundry Documentation](https://aka.ms/aistudio)
1. [Azure AI Templates with Azure Developer CLI](https://aka.ms/ai-studio/azd-templates)

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). Learn more here:

- [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/)
- [Microsoft Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
- Contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with questions or concerns

For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Responsible AI Guidelines

This project follows below responsible AI guidelines and best practices, please review them before using this project:

- [Microsoft Responsible AI Guidelines](https://www.microsoft.com/ai/responsible-ai)
- [Responsible AI practices for Azure OpenAI models](https://learn.microsoft.com/legal/cognitive-services/openai/overview)
- [Safety evaluations transparency notes](https://learn.microsoft.com/azure/ai-studio/concepts/safety-evaluations-transparency-note)

---
