CREATE OR REPLACE FUNCTION semantic_reranking(query TEXT, vector_search_results TEXT[])
RETURNS TABLE (article TEXT, relevance jsonb) AS $$
BEGIN
    RETURN QUERY
        WITH
        json_pairs AS(
        SELECT jsonb_build_object(
                    'pairs', 
                    jsonb_agg(
                        jsonb_build_array(query, article_)
                    )
                ) AS json_pairs_data
                FROM (
                    SELECT a.article as article_
                    FROM unnest(vector_search_results) as a(article)
                )
        ), 
        relevance_scores AS(
            SELECT jsonb_array_elements(invoke.invoke) as relevance_results
            FROM azure_ml.invoke(
                        (SELECT json_pairs_data FROM json_pairs),
                        deployment_name=>'bgev2m3-v1', timeout_ms => 120000)
        ),
        relevance_scores_rn AS (
            SELECT *, ROW_NUMBER() OVER () AS idx
            FROM relevance_scores
        )
        SELECT a.article,
               r.relevance_results
            FROM
                unnest(vector_search_results) WITH ORDINALITY AS a(article, idx2)
            JOIN
                relevance_scores_rn AS r(relevance_results, idx)
            ON
                a.idx2 = r.idx;

END $$ LANGUAGE plpgsql;
