# Add GraphRAG support in Azure Database for PostgreSQL

The Apache AGE extension in Azure Database for PostgreSQL offers a significant advancement that provides graph processing capabilities within the PostgreSQL ecosystem. This new extension brings a powerful toolset for developers looking to leverage a graph database with the robust enterprise features of Azure Database for PostgreSQL.

## What is Apache AGE?

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
