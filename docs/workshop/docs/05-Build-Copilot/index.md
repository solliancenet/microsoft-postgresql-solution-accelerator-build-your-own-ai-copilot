# Implement a Copilot

In this task, you will add an AI copilot to the _Woodgrove Bank Contract Management_ application using Python, the GenAI capabilities of Azure Database for PostgreSQL - Flexible Server, and the Azure AI extension. Using the AI-validated data, the copilot will use RAG to provide insights and answer questions about vendor contract performance and invoicing accuracy, serving as an intelligent assistant for Woodgrove Banks users.

## What are copilots?

Copilots are advanced AI assistants designed to augment human capabilities and improve productivity by providing intelligent, context-aware support, automating repetitive tasks, and enhancing decision-making processes. For instance, the Woodgrove Bank copilot will assist in data analysis, helping users identify patterns and trends in financial datasets.

## Why use Python?

Python's simplicity and readability make it a popular programming language for AI and machine learning projects. Its extensive libraries and frameworks, such as LangChain, FastAPI, and many others, provide robust tools for developing sophisticated copilots. Python's versatility allows developers to iterate and experiment quickly, making it a top choice for building AI applications.

## The RAG Pattern

The solution leverages the _Retrieval Augmented Generation_ (RAG) design pattern to ensure the copilot's responses are grounded in the (private) data maintained by Woodgrove Bank.

![RAG design pattern](../img/rag-design-pattern.png)

To understand how the RAG design pattern works in the context of the _Woodgrove Bank Contract Management_ application, select each tab in order and review the sequence of events shown in the figure above.

=== "1. Get Query"

    !!! info "The user query arrives at our copilot implementation via the chat API endpoint."
    
     User queries entered via the copilot interface of the _Woodgrove Bank Contract Management_ portal are sent to the backend API's `/chat` endpoint. The incoming "user query" has two components: the user _question_ (text input) and an optional _chat history_ (object array).

    The API extracts these parameters from the incoming request and invokes the `/chat` endpoint, starting the workflow that reflects this RAG design pattern.

=== "2. Vectorize Query"

    !!! info "Embeddings representing the user query are generated."
    
    The `/chat` endpoint sends the user request to Azure Database for PostgreSQL, where the `azure_ai` extension calls Azure OpenAI to vectorize the user's text input using a Large Language "Embedding" Model (e.g., Azure Open AI `text-embedding-3-large`). This vector is then used in the query to retrieve similar records in the next step.

=== "3. **Retrieve** Similar Data"

    !!! info "A hybrid search query is executed against the database to return semantically similar results."
    
    In this step, the vectorized query from the previous step is compared to data in relevant database tables to find and return _matching results_ based on exact full-text matches and vector similarity.
    
    !!! info "Improve RAG accuracy"
    
        The accuracy of the RAG pattern can also be improved by using database features like _semantic ranking_ to order the returned results and _GraphRAG_ to identify relationships between data, which you learn about in the next task.

=== "4. **Augment** Query"

    !!! info "The copilot augments user prompt with retrieved knowledge in request to model."
    
    The _Woodgrove Bank Contract Management_ application combines the user's original _question_ with hybrid search results returned from the database to create an enhanced or composite _model prompt_.

=== "5. **Generate** Response"

    !!! info "The chat model uses the prompt to generate a grounded response."
    
    The composite prompt, grounded with ("private") data, is sent to a Large Language "chat" completion model, such as Azure OpenAI's `gpt-4o`. The completion model sees the enhanced prompt (hybrid search results and chat history) as _grounding_ context for generating the final response, improving the quality (e.g., relevance, groundedness) of results returned from the Woodgrove Bank copilot.
