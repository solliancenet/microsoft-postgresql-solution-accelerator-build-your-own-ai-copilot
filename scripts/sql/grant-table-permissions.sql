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

    BEGIN
      EXECUTE format('GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO %I', username);
    EXCEPTION
      WHEN OTHERS THEN
        RAISE NOTICE 'Error granting privileges on sequences: %', SQLERRM;
    END;

    BEGIN
      EXECUTE format('GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO %I', username);
    EXCEPTION
      WHEN OTHERS THEN
        RAISE NOTICE 'Error granting privileges on functions: %', SQLERRM;
    END;
  ELSE
    RAISE NOTICE 'User % does not exist', username;
  END IF;
END $$ LANGUAGE plpgsql;