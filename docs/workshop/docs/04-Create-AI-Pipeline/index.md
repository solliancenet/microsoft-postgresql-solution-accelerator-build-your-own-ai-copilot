# AI-driven Data Validation

## Building an AI-Enhanced Data Ingestion and Processing Pipeline

An end-to-end data pipeline has been created to create an AI-powered solution for advanced data analysis. This pipeline starts with documents uploaded to Azure Blob Storage and employs Azure services for intelligent ingestion, automated validation, semantic analysis, and optimized storage.

AI-driven Data Validation offers a transformative solution by automating document processing, improving accuracy, and reducing the burden on human reviewers. Through a combination of intelligent document ingestion, machine learning, and natural language processing, AI will revolutionize how contract validation is performed.

In this section, you will enable a feature flag that will activate the AI components of the solution.


## NOTES: (to be removed)

2. Data ingestion
   1. Document Intelligence
      1. Utilize pre-built models in Azure Document Intelligence
      2. Configure semantic chunking
      3. Write chunks to Postgres, generating embeddings for each chunk on insert
      4. Update API endpoints for inserting chunks, or use an existing one (probably not yet created)
         1. Update API endpoint code to use a new query that handles embedding with the Azure AI extension.
   2. Data ingestion
      1. Data ingestion process is triggered when documents are uploaded through the application
          1. Document analysis step is triggered to ingest document and insert/update data in database
          1. Document validation step is triggered to validate the document and associated data within the database
              1. Invoices (more involved, validating dates, invoice totals, line item amounts, etc.)
                  1. Iterate through a few prompts, showing the process of getting it closer to what is desired for validation.
              1. SOWs (keep this simple, focused on looking for required sections and language)

## Validate documents

Create Python worker process that performs validation on document parts, comparing milestone pricing with invoiced amounts and work performed, looking for key SOW components such as compliance sections and wording, etc.

1. Perform embedding of document chunks/sections.

2. Use Azure OpenAI and GPT-4o models to do semantic similarity comparisons between key sections and expected language. Set a threshold similarity score to validate documents contain appropriate language.

    - Provide example document(s) with missing sections or incorrect and missing wording to show how these can be identified and flagged.
    - Provide good documents.

3. Insert text and associated embeddings into PostgreSQL.

4. Perhaps use a custom ML model to do numerical comparisons/analysis of project milestones + assigned dollar amount against invoices for the project?

    - Try with Azure OpenAI first, but it's not so good with numbers...