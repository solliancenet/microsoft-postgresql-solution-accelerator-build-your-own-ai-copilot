from app.functions.chat_functions import ChatFunctions
from app.lifespan_manager import get_chat_client, get_db_connection_pool, get_embedding_client, get_prompt_service
from app.models import CompletionRequest
from fastapi import APIRouter, Depends
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool

# Initialize the router
router = APIRouter(
    prefix = "/completions",
    tags = ["Completions"],
    dependencies = [Depends(get_chat_client)],
    responses = {404: {"description": "Not found"}}
)

@router.post('/chat', response_model = str)
async def generate_chat_completion(
    request: CompletionRequest,
    llm = Depends(get_chat_client),
    db_pool = Depends(get_db_connection_pool),
    embedding_client = Depends(get_embedding_client),
    prompt_service = Depends(get_prompt_service)):
    """Generate a chat completion using the Azure OpenAI API."""
        
    # Retrieve the copilot prompt
    system_prompt = prompt_service.get_prompt("copilot")

    # Provide the copilot with a persona using the system prompt.
    messages = [{ "role": "system", "content": system_prompt }]

    # Add the chat history to the messages list
    # Chat history provides context of previous questions and responses for the copilot.
    for message in request.chat_history[-request.max_history:]:
        messages.append({"role": message.role, "content": message.content})

    # Create a chat prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history", optional=True),
            ("user", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ]
    )

    # Get the chat functions
    cf = ChatFunctions(db_pool, embedding_client)

    # Define tools for the agent to retrieve data from the database
    tools = [
        # Hybrid search functions
        StructuredTool.from_function(coroutine=cf.find_invoice_line_items),
        StructuredTool.from_function(coroutine=cf.find_invoice_validation_results),
        StructuredTool.from_function(coroutine=cf.find_milestone_deliverables),
        StructuredTool.from_function(coroutine=cf.find_sow_chunks),
        StructuredTool.from_function(coroutine=cf.find_sow_validation_results),
        # Get invoice data functions
        StructuredTool.from_function(coroutine=cf.get_invoice_id),
        StructuredTool.from_function(coroutine=cf.get_invoice_line_items),
        StructuredTool.from_function(coroutine=cf.get_invoice_validation_results),
        StructuredTool.from_function(coroutine=cf.get_invoices),
        # Get SOW data functions
        StructuredTool.from_function(coroutine=cf.get_sow_chunks),
        StructuredTool.from_function(coroutine=cf.get_sow_id),
        StructuredTool.from_function(coroutine=cf.get_sow_milestones),
        StructuredTool.from_function(coroutine=cf.get_milestone_deliverables),
        StructuredTool.from_function(coroutine=cf.get_sow_validation_results),
        StructuredTool.from_function(coroutine=cf.get_sows),
        # Get vendor data functions
        StructuredTool.from_function(coroutine=cf.get_vendors),
    ]
    
    # Create an agent
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)
    completion = await agent_executor.ainvoke({"input": request.message, "chat_history": messages})
    return completion['output']
