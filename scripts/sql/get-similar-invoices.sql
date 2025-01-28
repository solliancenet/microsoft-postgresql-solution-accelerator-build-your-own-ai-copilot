CREATE OR REPLACE FUNCTION get_similar_invoices(query_text TEXT, max_results INT DEFAULT 5, vendor INT DEFAULT NULL, sow INT DEFAULT NULL)
RETURNS TABLE(
    id BIGINT,
    number TEXT,
    vendor_id BIGINT,
    sow_id BIGINT,
    amount NUMERIC,
    invoice_date DATE,
    payment_status VARCHAR(50),
    datestamp TIMESTAMP,
    result TEXT,
    validation_passed BOOLEAN,
    rank REAL
) AS $$
DECLARE 
	query_embedding vector(3072);
BEGIN
	query_embedding := (
		azure_openai.create_embeddings('embeddings', query_text, max_attempts => 5, retry_delay_ms => 500)::vector
	);

    RETURN QUERY
    SELECT i.id, i.number, i.vendor_id, i.sow_id, i.amount, i.invoice_date, i.payment_status, r.datestamp, r.result, r.validation_passed,
        CASE
            WHEN r.result ILIKE '%' || query_text || '%' THEN 0 -- Exact match ranks highest
            ELSE (r.embedding <=> query_embedding)::real
        END AS rank
    FROM invoices AS i
    INNER JOIN invoice_validation_results as r ON i.id = r.invoice_id -- Only get invoices that have validation results
	WHERE (i.vendor_id = vendor OR vendor IS NULL)
		AND (i.sow_id = sow OR sow IS NULL)
    ORDER BY rank ASC
	LIMIT max_results;
END $$ LANGUAGE plpgsql;