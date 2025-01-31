# AI-driven Data Validation

## Building an AI-Enhanced Data Ingestion and Processing Pipeline

An end-to-end data pipeline has been created to create an AI-powered solution for advanced data analysis. This pipeline starts with documents uploaded to Azure Blob Storage and employs Azure services for intelligent ingestion, automated validation, semantic analysis, and optimized storage.

AI-driven Data Validation offers a transformative solution by automating document processing, improving accuracy, and reducing the burden on human reviewers. Through a combination of intelligent document ingestion, machine learning, and natural language processing, AI will revolutionize how contract validation is performed.

Prior to the integration of AI into the data ingestion workflow, the application would require a lot of manual parsing and input of Invoice and SOW data into the application. This can be a time consuming and labor intensive process.

In this section, you will review the code that integrates AI components into the solution.

## Validate documents

The document ingestion workflow process performs document text extraction, validation on document parts, comparing milestone pricing with invoiced amounts and work performed, looking for key SOW components such as compliance sections and wording, etc.

1. Use Azure Document Intelligence to perform document text extraction, and Azure OpenAI to generate text embeddings of document chunks/sections that are inserted into the database.

2. Use Azure OpenAI and GPT-4o model along with PostgreSQL vector extensions to do semantic similarity comparisons between key sections and expected language. Set a threshold similarity score to validate documents contain appropriate language.

    - Provide example document(s) with missing sections or incorrect and missing wording to show how these can be identified and flagged.
    - Provide good documents.

3. Insert text and associated embeddings into PostgreSQL.

4. Perhaps use a custom ML model to do numerical comparisons/analysis of project milestones + assigned dollar amount against invoices for the project?

    - Try with Azure OpenAI first, but it's not so good with numbers...