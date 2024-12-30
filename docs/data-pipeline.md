# Data pipeline

## Create custom Document Intelligence model

1. TODO: Add steps for creating custom Document Intelligence models for SOWs and invoices, which extract key document parts.

2. Send documents into Document Intelligence using workflow triggered by documents being added to blob storage.

## Validate documents

Create Python worker process that performs validation on document parts, comparing milestone pricing with invoiced amounts and work performed, looking for key SOW components such as compliance sections and wording, etc.

1. Perform embedding of document chunks/sections.

2. Use Azure OpenAI and GPT-4o models to do semantic similarity comparisons between key sections and expected language. Set a threshold similarity score to validate documents contain appropriate language.

    - Provide example document(s) with missing sections or incorrect and missing wording to show how these can be identified and flagged.
    - Provide good documents.

3. Insert text and associated embeddings into PostgreSQL.

4. Perhaps use a custom ML model to do numerical comparisons/analysis of project milestones + assigned dollar amount against invoices for the project?

    - Try with Azure OpenAI first, but it's not so good with numbers...
    - 
