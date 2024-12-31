-- Use psql variable substitution to inject the managed identity name
DO $$ 
DECLARE
  identity_name TEXT := :'managed_identity_name';  -- Parameterized identity
BEGIN
  IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = identity_name) THEN
    EXECUTE format('GRANT ALL PRIVILEGES ON DATABASE %I TO %I', current_database(), identity_name);
    EXECUTE format('GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO %I', identity_name);
  END IF;
END $$;
