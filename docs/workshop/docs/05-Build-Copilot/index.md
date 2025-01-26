# Implement Copilot

With AI-validated data now in the system, the second part of the solution is to implement an AI copilot, which will allow users to ask questions and gain actionable insights over the data in the PostgreSQL database. The solution leverages the RAG architecture pattern. When users submit questions through the copilot's chat interface, the query is processed by the SPA Web App and sent to the API's `/chat` endpoint.

TODO: Add more to the below about performing a hybrid search against the database and augmenting the prompt with data from the database...

The API then communicates with Azure OpenAI to generate a prompt embedding, which is used to perform a vector search in the Azure Database for PostgreSQL Flexible Server. The search results are retrieved and used to generate a completion response containing AI-generated insights. This response is sent back to the API and displayed to the user, providing them with relevant and actionable information based on the data stored in the Postgres database. This process enables users to efficiently query and analyze large datasets, making it easier to derive meaningful insights and make informed decisions.

**Copilot chat**: An Azure OpenAI + LangChain copilot enables project managers and leadership to quickly get metrics, trends and processing timelines for contracts, SOWs, invoices, and vendors using a user friendly chat interface. Function calling via LangChain tools enables the copilot to implement a RAG (retrieval-augmented generation) pattern over data in the PostgreSQL database, using vector search to efficiently retrieve relevant documents and data.

1. Implement `/chat` endpoint
   1. Code will already be there.
   2. Update to pull prompt from JSON file (ensure this is included in deployment)
2. Iterate on copilot prompt to allow for insights to be derived from data
   1. Should be able to answer questions about vendors, invoices and their alignment with SOWs
   2. Test the endpoint...
4. Use LangChain (already in place, so will just need to review the code and go over the details.)
   1. Multi-agent approach?
   2. Autogen?
5. Implement RAG (Function calling review)
   1. Show how to use LangChain's `StructuredTool` (or whatever it is) to call existing functions to get info from the database for RAG
   2. Embed incoming user messages for similarity search and semantic ranker capablities
6. Enable Chat/Copilot UI in REACT app.
   1. Steps for this? 
      1. 

## The RAG Pattern

The solution leverages the _Retrieval Augmented Generation_ (RAG) design pattern to ensure the copilot's responses are grounded in the (private) data maintained by the enterprise, for this application.

![RAG design pattern](../img/rag-design-pattern.png)

Let's learn how this design pattern works in the context of our Contoso Chat application. Click on the tabs in order, to understand the sequence of events shown in the figure above.

---

=== "1. Get Query"

    !!! info "The user query arrives at our copilot implementation via the endpoint (API)"
    
    Our deployed Contoso Chat application is exposed as a hosted API endpoint using Azure Container Apps. The inoming "user query" has 3 components: the user _question_ (text input), the user's _customer ID_ (text input), and an optional _chat history_ (object array).
    
    The API server extracts these parameters from the incoming request, and invokes the Contoso Chat application - starting the workflow reflecting this RAG design pattern.

=== "2. Vectorize Query"

    !!! info "The copilot sends the text query to a **retrieval** service after first vectorizing it."
    
    The Contoso Chat application converts the text question into a vectorized query using a Large Language "Embedding" Model (e.g., Azure Open AI `text-embedding-ada-002`). This is then sent to the information retrieval service (e.g., Azure AI Search) in the next step.

=== "3. **Retrieve** Matches"

    !!! info "The retrieval service uses vectorized query to return matching results by similarity"
    
    The information retrieval service maintains a search index for relevant information (here, for our product catalog). In this step, we use the vectorized query from the previous step to find and return _matching product results_ based on vector similarity. The information retrieval service can also use features like _semantic ranking_ to order the returned results.

    ### Semantic Ranking
    TODO: Add details about semantic ranking and graph rag...

    TODO: Include details about SEMANTIC RANKER MODEL () and include in the text above
    - Update data and flow diagrams to talk about semantic ranker for custom model inference.
    - Blog post to use are reference: <https://techcommunity.microsoft.com/blog/adforpostgresql/introducing-the-semantic-ranking-solution-for-azure-database-for-postgresql/4298781>
    - Model to use: <https://huggingface.co/BAAI/bge-reranker-v2-m3>

    ### GraphRAG

    TODO

=== "4. **Augment** Query"

    !!! info "The copilot augments user prompt with retrieved knowledge in request to model"
    
    The Contoso Chat application combines the user's original _question_ with returned "documents" from the information retrieval service, to create an enhanced _model prompt_. This is made easier using prompt template technologies (e.g., Prompty) with placeholders - for chat history, retrieved documents, and customer profile information - that are filled in at this step.

=== "5. **Generate** Response"

    !!! info "The chat model uses prompt to generate a grounded response to user question."
    
    This enhanced prompt is now sent to the Large Language "chat" model (e.g., Azure OpenAI `gpt-35-turbo` or `gpt-4o`) which sees the enhanced prompt (retrieved documents, customer profile data, chat history) as _grounding_ context for generating the final response, improving the quality (e.g., relevance, groundedness) of results returned from Contoso Chat.
