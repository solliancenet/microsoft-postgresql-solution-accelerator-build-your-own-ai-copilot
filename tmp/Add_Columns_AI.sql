-- DDL for AI componentry (for invoices)

ALTER TABLE invoices
ADD content text;

ALTER TABLE invoices
ADD embeddings vector(3072);

ALTER TABLE sows
ADD embeddings vector(3072);

ALTER TABLE sows
ADD summary text;
