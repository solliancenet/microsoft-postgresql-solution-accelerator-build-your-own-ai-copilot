# 4. App Architecture

The objective of this solution is to automate the extraction, validation, and storage of invoices and SOWs to minimize manual effort and boost operational efficiency. This solution architecture facilitates seamless integration across multiple Azure services, ensuring scalability, security, and optimized costs, while accurately aligning invoices with milestone-based deliverables and other contractual obligations.

The high-level solution architecture is represented by the following diagrams:

## Data ingestion and validation architecture

The attached image is a detailed flowchart illustrating the architecture of a data ingestion and AI processing system integrated with an AI copilot using Retrieval-Augmented Generation (RAG). The system is divided into two main sections: "Data Ingestion & AI Processing" and "AI Copilot with RAG." The flowchart shows how users interact with the system, how data is processed, and how AI-generated insights are delivered back to the users.

![](./../img/data-ingestion-validation-architecture-diagram.png)

## Copilot architecture

The second part of the application is an AI copilot, which allows users to ask questions and gain actionable insights over the data in the PostgreSQL database by leveraging a RAG architecture pattern. When users submit  questions through the Copilot's chat interface, the query is processed by the SPA Web App and sent to the API. The API then communicates with Azure OpenAI to generate a prompt embedding, which is used to perform a vector search in the Azure Database for PostgreSQL Flexible Server. The search results are retrieved and used to generate a completion response containing AI-generated insights. This response is sent back to the API and displayed to the user, providing them with relevant and actionable information based on the data stored in the Postgres database. This process enables users to efficiently query and analyze large datasets, making it easier to derive meaningful insights and make informed decisions.

![](./../img/copilot-architecture-diagram.png)

The attached image is a flowchart illustrating the architecture of an AI Copilot with Retrieval-Augmented Generation (RAG). The flowchart shows how users interact with the system through a browser-based Copilot Chat interface. The users' queries are sent to a Single Page Application (SPA) Web App, which communicates with an API. The API interacts with Azure OpenAI to generate prompt embeddings and perform vector searches. The vector search results are retrieved from an Azure Database for PostgreSQL Flexible Server (Vector Store). The completion response, which contains AI-generated insights, is then sent back to the API and displayed to the users through the SPA Web App. The system also includes components like Key Vault and Azure App Configuration for secure and efficient management of application settings and secrets.

## Information flow diagram

Tying the two architecture components together...

![High-level architecture diagram for the solution](./../img/solution-flow-diagram.png)

### Into the System

1. Users upload documents, such as SOWs and invoices, through a Single Page Application (SPA) via a web browser.
2. The SPA web app communicates directly with a backend API.
3. The API saves uploaded documents into a Blob Storage container.
4. When new documents are added into blob storage an Event Grid trigger is fired, which launches a Data Ingestion Worker Process. This worker process sends the uploaded documents to the Azure AI Document Intelligence service, which uses custom models to efficiently extract text and structure from the documents. Using the built in semantic chunking capability of Document Intelligence, document content is chunked based on document structures, capturing headings and chunking the content body based on semantic coherence, such as paragraphs and sentences, ensuring the chunks are of higher quality for use in RAG pattern queries.
5. Once processed, the data is validated by a Validation worker process, which uses Azure OpenAI to validate the incoming data conforms to expected standards and is accurate based on other data already in the system.
   1. Call out the Azure AI extension & GraphRAG & Apache AGE
6. The output from the Document Ingestion and Validation worker processes is written into Azure Database for PostgreSQL flexible server, which serves as both a relation database and vector store. The data is accessible for further analysis. Azure OpenAI is utilized to generate text embeddings, which are stored for efficient retrieval during the querying process.

### Out of the System

7. Users interact with a Copilot Chat through a browser interface to pose queries or seek information.
8. These chat requests are sent to the SPA Web App and then to the API.
9. The request query is embedded using the `text-embedding-3-large` model in Azure OpenAI.
10. A hybrid search is performed on the Azure Database for PostgreSQL Flexible Server, where the system searches for relevant data using the previously generated embeddings.
11. The search results are combined with additional data if necessary and used to generate a comprehensive response.
12. This AI-generated completion response is then sent back to the user through the browser interface, providing them with actionable insights based on the data stored in the system. The efficient flow of information ensures users can quickly and accurately obtain the information they need.

TODO: Include details about SEMANTIC RANKER MODEL () and include in the text above
    - Update data and flow diagrams to talk about semantic ranker for custom model inference.
    - Blog post to use are reference: <https://techcommunity.microsoft.com/blog/adforpostgresql/introducing-the-semantic-ranking-solution-for-azure-database-for-postgresql/4298781>
    - Model to use: <https://huggingface.co/BAAI/bge-reranker-v2-m3>

Click on each tab to understand the archtiecture components and processing workflow.

---

=== "1. Architecture Components"

    The architecture has these core components:
    
    - _UI_ → the **user interface** for interacting with the system
    - _API_ → a Python API for integrating backend services
    - _Azure Database for PostgreSQL_ → the project **database** (vendors, invoices, statements of work (SOWs))
    - _Azure OpenAI_ → the **model deployments** (embedding, chat, eval)
    - _Azure Container Apps_ → the **app hosting** service (API endpoint)
    - _Azure Managed Identity_ → for **keyless authentication** (trustworthy AI)

=== "2. Processing Services"

    The Architecture "processes" incoming user requests received on the hosted API endpoint by taking the following steps:

    1. **Data Ingestion**: SOWs, invoices and other related documents are ingested via a custom REACT web application. Internal users and external vendors can submit documents by uploading them through the web app, which then uploads them to Azure Blob Storage.

    2. **Workflow Trigger Mechanism**: Upon receipt of new documents, an event trigger activates Python-based background worker processes:

        a. **Data Extraction and Processing**: Azure's OCR (Optical Character Recognition) technology digitizes content from uploaded documents, such as SOWs and invoices.
    
        b. **Document Intelligence (Custom Model)**: A custom AI model within Azure's Document Intelligence service is tailored to extract specific data fields, like payment milestones, dates, amounts, and vendor details. This model is trained to recognize the structure of financial documents, improving data extraction accuracy.

        c. **Confidence Scoring and Validation**: Each document is assigned a confidence score based on whether the documents contain the correct sections and fields.

        d. **Validation Using Azure OpenAI**: Azure OpenAI language models, such as GPT-4o, are used to review all document data, employing natural language understanding to validate and cross-check information, ensuring high data integrity. The language model is used to cross-reference data between invoices and SOWs, evaluating payment milestone completion and billing, and preventing issues like payment delays. It also validates that appropriate compliance language exists in contracts and SOWs, helping to avoid compliance violations.

    3. **Secure Storage and Database Management**: Validated data is chunked, vectorized using an Azure OpenAI embedding model, and stored in an encrypted Azure Database for PostgreSQL flexible server database, which uses vector embeddings for advanced search and retrieval. This supports efficient handling of structured and semi-structured data, facilitating downstream analytics. Azure Database for PostgreSQL flexible server supports JSON-based semi-structured data and vector embedding storage, enabling AI-enhanced queries. Embeddings can be generated directly from database queries using the Azure AI extension for PostgreSQL.

    4. **Document enrichment**: The Azure AI extension for PostreSQL also enables data to be enhanced using Azure AI Services directly from the database. This capability provides rich AI functionality, such as text translation and entity and keyword extraction.

    5. **Copilot chat**: An Azure OpenAI + LangChain copilot enables project managers and leadership to quickly get metrics, trends and processing timelines for contracts, SOWs, invoices, and vendors using a user friendly chat interface. Function calling via LangChain tools enables the copilot to implement a RAG (retrieval-augmented generation) pattern over data in the PostgreSQL database, using vector search to efficiently retrieve relevant documents and data.
