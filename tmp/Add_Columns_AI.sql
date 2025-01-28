-- DDL for AI componentry (for invoices)

CREATE EXTENSION IF NOT EXISTS azure_ai;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS age;

SELECT azure_ai.set_setting('azure_openai.endpoint', 'https://<endpoint>.openai.azure.com');
SELECT azure_ai.set_setting('azure_openai.subscription_key', '<api-ey>');

SELECT azure_ai.set_setting('azure_cognitive.endpoint', '{endpoint}');
SELECT azure_ai.set_setting('azure_cognitive.subscription_key', '{api-key}');




ALTER TABLE invoices
ADD content text;

ALTER TABLE invoices
ADD embeddings vector(3072);

ALTER TABLE sows
ADD embeddings vector(3072);

ALTER TABLE sows
ADD summary text;
