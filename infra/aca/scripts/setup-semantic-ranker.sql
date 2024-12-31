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
