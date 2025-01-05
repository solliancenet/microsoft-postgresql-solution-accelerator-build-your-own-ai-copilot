DO $$
DECLARE
  username text := '${env:SERVICE_API_IDENTITY_PRINCIPAL_NAME}';
BEGIN
  IF EXISTS (SELECT 1 FROM pg_user u WHERE u.usename = username) THEN
    BEGIN
      EXECUTE format('GRANT ALL PRIVILEGES ON DATABASE %I TO %I', current_database(), username);
    EXCEPTION
      WHEN OTHERS THEN
        RAISE NOTICE 'Error granting privileges on database: %', SQLERRM;
    END;

    BEGIN
      EXECUTE format('GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO %I', username);
    EXCEPTION
      WHEN OTHERS THEN
        RAISE NOTICE 'Error granting privileges on tables: %', SQLERRM;
    END;
  END IF;
END $$;