from app.functions.chat_functions import ChatFunctions
from app.lifespan_manager import get_chat_client, get_db_connection_pool, get_embedding_client, get_prompt_service
from app.models import CompletionRequest, CompletionResponse
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

@router.post('/chat', response_model=CompletionResponse)
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

    # Get the chat session ID
    session_id = request.session_id

    # Create a chat session if one does not exist
    if (session_id == None or session_id <= 0):
        # if session_id is not provided or -1, create a new chat session
        async with db_pool.acquire() as conn:
            session_id = await create_chat_session(conn, request.message[:50])

    # Add the chat history to the messages list for the session
    # Chat history provides context of previous questions and responses for the copilot.
    async with db_pool.acquire() as conn:
        chat_history = await get_chat_history(conn, session_id)
        for message in chat_history[-request.max_history:]:
            messages.append({"role": message["role"], "content": message["content"]})
   

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
        StructuredTool.from_function(coroutine=cf.get_vendors)
    ]
    
    # Create an agent
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)
    completion = await agent_executor.ainvoke({"input": request.message, "chat_history": messages})
    completionOutput = completion['output']

    # Write the chat history to the database
    async with db_pool.acquire() as conn:
        await write_chat_history(conn, session_id, "user", request.message)
        await write_chat_history(conn, session_id, "assistant", completionOutput)

    # Return the completion output
    return CompletionResponse(
        session_id = session_id,
        content = completionOutput
    )

@router.get('/sessions')
async def get_chat_sessions(
    db_pool = Depends(get_db_connection_pool)
    ):
    """Retrieves a list of chat sessions."""
    sessions = []
    async with db_pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM copilot_chat_sessions ORDER BY datestamp DESC;')
        for row in rows:
            sessions.append({"id": row["id"], "name": row["name"]})
    return sessions

@router.get('/history/{session_id}')
async def get_chat_history(
    session_id: int,
    db_pool = Depends(get_db_connection_pool)
    ):
    """Retrieves the chat history for a chat session."""
    messages = []
    async with db_pool.acquire() as conn:
        chat_history = await get_chat_history(conn, session_id)
        for message in chat_history:
            messages.append({"role": message["role"], "content": message["content"]})
    return messages

@router.delete('/sessions/{session_id}')
async def delete_chat_session(
    session_id: int,
    db_pool = Depends(get_db_connection_pool)
    ):
    """Deletes a chat session."""
    async with db_pool.acquire() as conn:
        await conn.execute('DELETE FROM copilot_chat_session_history WHERE copilot_chat_session_id = $1;', session_id)
        await conn.execute('DELETE FROM copilot_chat_sessions WHERE id = $1;', session_id)
    return {"status": "success"}

async def get_chat_history(conn, session_id: int):
    rows = await conn.fetch(
        """
        SELECT role, content
        FROM copilot_chat_session_history
        WHERE copilot_chat_session_id = $1
        ORDER BY datestamp
        """,
        session_id
    )
    return rows

async def create_chat_session(conn, name: str):
    session_id = await conn.fetchval(
        """
        INSERT INTO copilot_chat_sessions
        (name)
        VALUES (
            $1
        )
        RETURNING id;
        """, name)
    return session_id

async def write_chat_history(conn, session_id: int, role: str, content: str):
    await conn.execute(
        """
        INSERT INTO copilot_chat_session_history (copilot_chat_session_id, role, content)
        VALUES ($1, $2, $3)
        """,
        session_id, role, content
    )