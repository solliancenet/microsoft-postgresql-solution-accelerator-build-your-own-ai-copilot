# Improve RAG Accuracy

TODO: Add intro explaining how RAG can be improved using techniques like Semantic Ranking and GraphRAG.

The success of Generative AI apps in the enterprise is frequently decided by the amount of trust their users can put into them, which is, in turn, measured by the accuracy of their responses. When GenAI apps deliver precise, fact-based responses, users can rely on them for insightful, accurate information. This is why we are excited to announce Generally Availability of the new Semantic Ranking Solution Accelerator for Azure Database for PostgreSQL, offering a powerful boost to the accuracy of GenAI apps’ information retrieval pipeline by reranking vector search results with semantic ranking models.

Many businesses today are being reimagined from the ground up starting from the new foundation of Generative AI technology. The key challenge these innovators face is ensuring the trust of the users in the new platform. To achieve that, GenAI apps need to become much more accurate and precise in their responses than they are today. This is why we are excited to announce the Public Preview of GraphRAG Solution Accelerator for Azure Database for PostgreSQL!

## The problem of accuracy

Innovation in the GenAI space is moving fast. Only recently we were introduced to ChatGPT and we learned that it can hallucinate and make up answers. This put an initial dent in our trust in GenAI apps. But the industry quickly came up with a solution – the Retrieval Augmented Generation (RAG) approach. RAG apps use facts gathered from enterprise or internal data sources of the user to ground LLM model responses in factual data and improve their accuracy. The technique delivers great immediate results in initial POCs and small-scale deployments. But when the number of documents grows or the documents are too similar to each other, the fact gathering engine of the RAG apps – the vector search - starts to fail. We hear from many customers that progressed from the initial POC step to production deployment that the solution is almost there but its accuracy is still too low. The productivity loss from the incorrect answers and the loss of user trust are just too big to ignore. For these experienced customers the question of deploying RAG apps quickly becomes the question of whether they can boost the accuracy of the GenAI app to an acceptable level.

GenAI has come far, but accuracy remains a challenge. Retrieval Augmented Generation (RAG) helps by grounding responses in factual data, but as datasets grow or when documents are too similar to each other, its vector search can falter, leading to users losing trust and the promise of improved productivity evaporating. Improving accuracy requires optimizing the information retrieval pipeline with techniques ranging from general methods like chunking, larger embeddings, and hybrid search, to advanced, dataset-specific approaches like semantic ranking, RAPTOR summarization, and GraphRAG. The effectiveness of these techniques depends on the dataset, so investing in a robust evaluation framework is critical as well.



=== "Semantic Ranking"

    TODO: Explain this

    In this blog we focus on the semantic ranking technique - one of the more universally applicable techniques - and discuss details of the provided Solution Accelerator for Azure Database for PostgreSQL.

    Semantic ranker works by comparing two strings of text: the search query and the text of one of the items it is searching over. The ranker produces a relevance score indicating whether these two text strings are relevant to each other, or, in other words, if the text holds an answer to the query. The semantic ranker is a machine learning model. Usually, it is one of the variants of the BERT language model fine-tuned to perform the ranking task, as illustrated below. The ranker model can also be an LLM. The ranker model takes as input two strings and outputs one relevance score, usually a number in the range of 0 to 1. For that reason, this type of model is also called a cross-encoder model.

    Compared to vector search, which simply measures vector similarity between two vector embeddings, the semantic ranker model goes down to the level of the actual text and performs deeper analysis of the semantic relevance between two text strings. This gives the semantic ranker a potential to produce more accurate results. The actual accuracy of the semantic ranker model is dependent on its size, what data it was fine-tuned on and how compatible it is with the dataset it is being used on. For this Solution Accelerator we benchmarked open-source semantic ranker models to pick the best one for deployment.

    The semantic ranker solution accelerator for Azure Database for PostgreSQL enables a significant improvement in the accuracy of the information retrieval pipelines of Generative AI apps. By leveraging the power of semantic ranking, businesses can achieve unprecedented accuracy in data retrieval and ensure success of their Generative AI investments. As this technology continues to evolve, it promises to unlock new opportunities and drive GenAI innovation across various sectors.

=== "GraphRAG"

    The Apache AGE extension in Azure Database for PostgreSQL offers a significant advancement that provides graph processing capabilities within the PostgreSQL ecosystem. This new extension brings a powerful toolset for developers looking to leverage a graph database with the robust enterprise features of Azure Database for PostgreSQL.
    
    TODO: Use this blob post as a guide: https://techcommunity.microsoft.com/blog/adforpostgresql/introducing-the-graphrag-solution-for-azure-database-for-postgresql/4299871
    
    3. Add GraphRAG functionality
       1. Provide graph nodes for relationships between SOWs, vendors, and invoices. Also, linking invoice line items with milestones and deliverables in SOWs?
    
    ### What is Apache AGE?
    
    [Apache Graph Extension](https://age.apache.org/age-manual/master/index.html) (AGE) is a PostgreSQL extension developed under the Apache Incubator project. It is designed to provide graph database functionality, enabling users to store and query graph data efficiently within PostgreSQL. It supports the openCypher query language, which allows for intuitive and expressive graph queries. With AGE, you can manage and analyze complex relationships within your data, uncovering insights that traditional relational databases and even semantic search might miss.
    
    ---
    
    !!! info "Click on the tabs below to understand the key features and benefits of using AGE in Azure Database for PostgreSQL."
    
    === "Key Features"
    
        - Graph and Relational Data Integration: AGE allows seamless integration of graph data with existing relational data in PostgreSQL. This hybrid approach enables you to benefit from both graph and relational models simultaneously.
        - openCypher Query Language: AGE incorporates openCypher, a powerful and user-friendly query language specifically designed for graph databases. This feature simplifies the process of writing and executing graph queries.
        - High Performance: AGE is optimized for performance, ensuring efficient storage and retrieval of graph data thanks to support for indexing of graph properties using GIN indices.
        - Scalability: Built on PostgreSQL's proven architecture, AGE inherits its scalability and reliability, allowing it to handle growing datasets and increasing workloads.
    
    === "Benefits"
    
        The integration of AGE in Azure Database for PostgreSQL brings numerous benefits to developers and businesses looking to leverage graph processing capabilities:
    
        - Simplified Data Management: AGE's ability to integrate graph and relational data simplifies data management tasks, reducing the need for separate graph database solutions.
        - Enhanced Data Analysis: With AGE, you can perform complex graph analyses directly within your PostgreSQL database, gaining deeper insights into relationships and patterns in your data.
        - Cost Efficiency: By utilizing AGE within Azure Database for PostgreSQL, you can consolidate your database infrastructure, lowering overall costs and reducing the complexity of your data architecture.
        - Security and Compliance: Leverage Azure's industry-leading security and compliance features, ensuring your graph data is protected and meets regulatory requirements.
