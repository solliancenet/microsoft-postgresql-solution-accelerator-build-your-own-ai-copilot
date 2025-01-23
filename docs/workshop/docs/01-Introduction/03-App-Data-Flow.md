# 3. Application Data Flow

The solution automates the extraction, validation, and storage of invoices and SOWs to minimize manual effort and boost operational efficiency, while also allowing internal application users to gain actionable insights from the data. To achieve this, it is crucial to understand the flow of information through the system:

1. **User Actions and Data Upload**: Users upload documents, such as invoices and SOWs, into the system.
2. **Data Pipeline for Automated Ingestion**: The uploaded documents enter a data pipeline that automates data ingestion into the database.
3. **AI-Driven Data Validation**: During the ingestion process, AI services validate the extracted data to ensure accuracy and alignment with contract requirements.
4. **Data Storage**: Validated data is securely stored in the Azure Database for PostgreSQL.
5. **Access and Insights via Copilot**: Internal users access the stored data through a copilot, which employs the Retrieval Augmented Generation (RAG) pattern. This copilot provides intelligent assistance by offering insights into contract data based on the private data maintained by the enterprise.

By focusing on this streamlined flow, the solution effectively automates tedious tasks, reduces errors, and provides valuable insights to internal users, enhancing overall operational efficiency and decision-making. The following diagram illustrates the flow of information though the system, from data ingestion to AI processing and validation to actionable insights.

![High-level architecture diagram for the solution](./../img/solution-flow-diagram.png)

_Click each tab below to learn more about how the movement of data in the context of the Woodgrove Bank application!_

== "Into the System"

    1. Users upload documents, such as SOWs and invoices, through a Single Page Application (SPA) via a web browser.
    2. The SPA web app communicates directly with a backend API.
    3. The API saves uploaded documents into a Blob Storage container.
    4. When new documents are added into blob storage an Event Grid trigger is fired, which launches a Data Ingestion Worker Process. This worker process sends the uploaded documents to the Azure AI Document Intelligence service, which uses custom models to efficiently extract text and structure from the documents. Using the built in semantic chunking capability of Document Intelligence, document content is chunked based on document structures, capturing headings and chunking the content body based on semantic coherence, such as paragraphs and sentences, ensuring the chunks are of higher quality for use in RAG pattern queries.
    5. Once processed, the data is validated by a Validation worker process, which uses Azure OpenAI to validate the incoming data conforms to expected standards and is accurate based on other data already in the system.
    6. Call out the Azure AI extension & GraphRAG & Apache AGE
    7. The output from the Document Ingestion and Validation worker processes is written into Azure Database for PostgreSQL flexible server, which serves as both a relation database and vector store. The data is accessible for further analysis. Azure OpenAI is utilized to generate text embeddings, which are stored for efficient retrieval during the querying process.

=== "Out of the System"

    1. Users interact with a Copilot Chat through a browser interface to pose queries or seek information.
    2. These chat requests are sent to the SPA Web App and then to the API.
    3. The request query is embedded using the `text-embedding-3-large` model in Azure OpenAI.
    4.  A hybrid search is performed on the Azure Database for PostgreSQL Flexible Server, where the system searches for relevant data using the previously generated embeddings.
    5.  The search results are combined with additional data if necessary and used to generate a comprehensive response.
    6.  This AI-generated completion response is then sent back to the user through the browser interface, providing them with actionable insights based on the data stored in the system. The efficient flow of information ensures users can quickly and accurately obtain the information they need.
