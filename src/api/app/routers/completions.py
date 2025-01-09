from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool

from app.lifespan_manager import get_chat_client, get_db_connection_pool
from app.models import CompletionRequest, Vendor
from fastapi import APIRouter, Depends, HTTPException

# Initialize the router
router = APIRouter(
    prefix = "/completions",
    tags = ["Completions"],
    dependencies = [Depends(get_chat_client)],
    responses = {404: {"description": "Not found"}}
)

async def get_system_prompt():
    """Retrieves the copilot system prompt from the database."""
    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        # select first prompt value
        row = await conn.fetchrow('SELECT * FROM prompts WHERE id = $1;', 'COPILOT_SYSTEM_PROMPT')
        if row is None:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return row['prompt']

@router.post('/chat', response_model = str)
async def generate_chat_completion(request: CompletionRequest, llm = Depends(get_chat_client)):
    """Generate a chat completion using the Azure OpenAI API."""
        
    # Example of the system prompt that contains the assistant's persona.
    # system_prompt = """
    # You are an intelligent copilot for Woodgrove Bank designed to help users gain insights from vendor statements of work (SOWs) and invoices.
    # You are helpful, friendly, and knowledgeable, but can only answer questions about Woodgrove's contracts and associated invoices.
    # """

    # Load Copilot System Prompt from database
    system_prompt = await get_system_prompt()

    # Provide the copilot with a persona using the system prompt.
    messages = [{ "role": "system", "content": system_prompt }]

    # Add the chat history to the messages list
    for message in request.chat_history[-request.max_history:]:
        messages.append(message)

    # Add the current user message to the messages list
    messages.append({"role": "user", "content": request.message})

    # Create a chat prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history", optional=True),
            ("user", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ]
    )
    
    # TODO: Define tools for the agent
    tools = [
        StructuredTool.from_function(coroutine=get_invoices),
        StructuredTool.from_function(coroutine=get_msas),
        StructuredTool.from_function(coroutine=get_sows),
        StructuredTool.from_function(coroutine=get_vendors)         
    ]
    
    # Create an agent
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)
    completion = await agent_executor.ainvoke({"input": request.message, "chat_history": request.chat_history[-request.max_history:]})
    return completion['output']

async def get_invoices():
    """Retrieves a list of invoices from the database."""
    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM invoices;')
        invoices = [dict(row) for row in rows]
    return invoices

async def get_msas():
    """Retrieves a list of master services agreements (MSAs) from the database."""
    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM msas;')
        msas = [dict(row) for row in rows]
    return msas

async def get_sows():
    """Retrieves a list of statements of work (SOWs) from the database."""
    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM sows;')
        sows = [dict(row) for row in rows]
    return sows

async def get_vendors():
    """Retrieves a list of vendors from the database."""
    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM vendors;')
        vendors = [Vendor(**dict(row)) for row in rows]
    return vendors