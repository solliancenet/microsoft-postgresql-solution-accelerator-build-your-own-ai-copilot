# PostgreSQL Solution Accelerator: Build your own AI Copilot / FSI Scenario

In the financial services industry, validating contracts, statements of work (SOWs), and invoices poses distinct challenges. This is particularly true when it comes to ensuring that invoices align with SOWs, especially for milestone-based payments and other specific deliverables. Traditionally, this validation process is manual, requiring meticulous comparison and cross-checking, often leading to delays, errors, and elevated operational costs. This article explores a high-level architectural solution utilizing Microsoft Azure's comprehensive suite of services to automate and streamline this process, resulting in faster, more accurate, and cost-effective invoice validation.

## Solution Architecture

The objective of this solution is to automate the extraction, validation, and storage of invoices and SOWs to minimize manual effort and boost operational efficiency. This solution architecture facilitates seamless integration across multiple Azure services, ensuring scalability, security, and optimized costs, while accurately aligning invoices with milestone-based deliverables and other contractual obligations.

The high-level solution architecture is represented by this diagram:

![High-level architecture diagram for the solution](./media/solution-architecture-diagram.png)

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
