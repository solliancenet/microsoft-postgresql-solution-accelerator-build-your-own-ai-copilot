DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'azure_ai') THEN
    CREATE EXTENSION azure_ai;
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN
    CREATE EXTENSION vector;
  END IF;
END $$;

select azure_ai.set_setting('azure_openai.endpoint', '${env:AZURE_OPENAI_ENDPOINT}');
select azure_ai.set_setting('azure_openai.subscription_key', '${env:AZURE_OPENAI_KEY}');
