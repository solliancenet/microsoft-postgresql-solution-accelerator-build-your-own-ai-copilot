# Implement Copilot

1. Implement `/chat` endpoint
2. Create prompt to allow for insights to be derived from data
   1. Should be able to answer questions about vendors, invoices and their alignment with SOWs
   2. Update the `/chat` endpoint with the prompt
   3. Test the endpoint...
3. Add GraphRAG functionality
   1. Provide graph nodes for relationships between SOWs, vendors, and invoices. Also, linking invoice line items with milestones and deliverables in SOWs?
4. Use LangChain (already in place, so will just need to review the code and go over the details.)
   1. Multi-agent approach?
   2. Autogen?
5. Implement RAG (Function calling review)
   1. Show how to use LangChain's `StructuredTool` (or whatever it is) to call existing functions to get info from the database for RAG
   2. Embed incoming user messages for similarity search and semantic ranker capablities
6. Enable Chat/Copilot UI in REACT app.
