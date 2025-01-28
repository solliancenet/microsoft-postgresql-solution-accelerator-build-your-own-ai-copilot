from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from typing import Literal
from datetime import datetime, timezone

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

@router.post('/chat', response_model = str)
async def generate_chat_completion(request: CompletionRequest, llm = Depends(get_chat_client)):
    """Generate a chat completion using the Azure OpenAI API."""
        
    # Example of the system prompt that contains the assistant's persona.
    system_prompt = f"""
    You are an intelligent copilot for Woodgrove Bank designed to help users gain insights about vendors, their performance, and accuracy in delivering on statements of work (SOWs) and invoices.
    You are helpful, friendly, and knowledgeable, but can only answer questions about Woodgrove's contracts and associated invoices.

    If asked about a specific vendor, always provide information about the vendor, their SOWs, and invoices.
    If asked about a specific SOW, always provide information about the SOW, its associated invoices, and the vendor.
    If asked about a specific invoice, always provide information about the invoice, its associated SOW, and the vendor.

    Always provide a description of the vendor, including the type of services they provide and their contact information.

    When asked about a vendor's performance or billing accuracy:
    - Use validation results for SOWs and invoices to perform your analysis.
    - Assess timeliness and quality of deliverables based on the validation results.
    - Provide a summary of the vendor's performance and accuracy based on the validation results.
    - Your response should include only your assessment, without any invoice and SOW data, unless specifically asked otherwise.
    """

    """ Probably not needed for this prompt...
    For context, today is {datetime.now(timezone.utc).strftime('%A, %B %d, %Y')}.
    """

    # Provide the copilot with a persona using the system prompt.
    messages = [{ "role": "system", "content": system_prompt }]

    # Add the chat history to the messages list
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
    
    # TODO: Define tools for the agent
    tools = [
        StructuredTool.from_function(coroutine=get_vendors),
        StructuredTool.from_function(coroutine=get_invoices),
        StructuredTool.from_function(coroutine=get_similar_invoice_validation_results),
        StructuredTool.from_function(coroutine=get_sows)
    ]
    
    # Create an agent
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)
    completion = await agent_executor.ainvoke({"input": request.message, "chat_history": messages})
    return completion['output']

async def get_invoices(vendor_id: int = None, sow_id: int = None):
    """
    Retrieves a list of invoices from the database for a specified vendor or sow.
    If no vendor_id or sow_id is provided, all invoices are returned.
    """
    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        tables = {
            "invoices": {
                "name": "invoices",
                "alias": "i",
                "columns": ["id", "number", "vendor_id", "sow_id", "amount", "invoice_date", "payment_status"],
            },
            "invoice_line_items": {
                "name": "invoice_line_items",
                "alias": "l",
                "columns": ["description", "amount"],
            }
        }

        # Create columns list from both tables
        columns = [f"{tables[table]['alias']}.{column}" for table in tables for column in tables[table]['columns']]
        # Build a SELECT query and JOIN from the tables and columns
        query = f'SELECT {",".join(columns)} FROM {tables["invoices"]["name"]} AS {tables["invoices"]["alias"]}'
        # Join the invoice line items table
        query += f' LEFT JOIN {tables["invoice_line_items"]["name"]} AS {tables["invoice_line_items"]["alias"]} ON {tables["invoices"]["alias"]}.id = {tables["invoice_line_items"]["alias"]}.invoice_id'
        
        if vendor_id is not None:
            query += f' WHERE {tables["invoices"]["alias"]}.vendor_id = {vendor_id}'
            if sow_id is not None:
                query += f' AND {tables["invoices"]["alias"]}.sow_id = {sow_id}'    
        elif sow_id is not None:
            query += f' WHERE {tables["invoices"]["alias"]}.sow_id = {sow_id}'

        rows = await conn.fetch(f'{query};')
        invoices = [dict(row) for row in rows]
    return invoices

async def get_similar_invoice_validation_results(user_query: str, vendor_id: int = None):
    """
    Retrieves invoice accuracy and performance validation results similar to the user query for the specified vendor.
    If no vendor_id is provided, invoice validation results for all vendors are returned.
    """
    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        # if query is not None:
        #     rows = await conn.fetch('''
        #         WITH
        #         retrieval_result AS(
        #             SELECT id
        #             FROM invoices
        #             ORDER BY
        #                 invoices.embedding <=> azure_openai.create_embeddings('embeddings', $1, throw_on_error => FALSE, max_attempts => 1000, retry_delay_ms => 2000)::vector
        #             LIMIT 10
        #         )
        #         SELECT i.* FROM semantic_reranking($1, array (SELECT id FROM retrieval_result)) ranking
        #         JOIN invoices i ON ranking.id = i.id
        #         ORDER BY relevance DESC limit 3;
        #     ''')
        # else:

        if vendor_id is not None:
            query = f"SELECT * FROM get_ranked_invoices('{user_query}', {vendor_id});"
        else:
            query = f"SELECT * FROM get_ranked_invoices('{user_query}');"
        
        rows = await conn.fetch(query)
        invoices = [dict(row) for row in rows]
    return invoices

async def get_sows(vendor_id: int = None): #, intent: Literal['', 'performance', 'accuracy'] = ''):
    """
    Retrieves a list of statements of work (SOWs) from the database for the specified vendor.
    If no vendor_id is provided, all SOWs are returned.
    """
    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        tables = {
            "sows": {
                "name": "sows",
                "alias": "s",
                "columns": ["id", "number", "vendor_id", "start_date", "end_date", "budget", "document"],
            },
            # "sow_chunks": {
            #     "name": "sow_chunks",
            #     "alias": "c",
            #     "columns": ["heading", "content", "page_number"],
            # },
            "milestones": {
                "name": "milestones",
                "alias": "m",
                "columns": ["name", "status"]
            },
            # "deliverables": {
            #     "name": "deliverables",
            #     "alias": "d",
            #     "columns": ["milestone_id", "description", "amount", "status", "due_date"]
            # }
        }

        # Create columns list from both tables
        columns = [f"{tables[table]['alias']}.{column}" for table in tables for column in tables[table]['columns']]
        # Build a SELECT query and JOIN from the tables and columns
        query = f'SELECT {", ".join(columns)} FROM {tables["sows"]["name"]} AS {tables["sows"]["alias"]}'
        # Join the related tables
        for table in tables:
            # Perform LEFT JOIN on the related tables
            if table != "sows":
                query += f' LEFT JOIN {tables[table]["name"]} AS {tables[table]["alias"]} ON {tables["sows"]["alias"]}.id = {tables[table]["alias"]}.sow_id'

        #query += f' LEFT JOIN {tables["milestones"]["name"]} AS {tables["milestones"]["alias"]} ON {tables["sows"]["alias"]}.id = {tables["milestones"]["alias"]}.sow_id'
        #query += f' LEFT JOIN {tables["deliverables"]["name"]} AS {tables["deliverables"]["alias"]} ON {tables["milestones"]["alias"]}.id = {tables["deliverables"]["alias"]}.milestone_id'
        #query += f' LEFT JOIN {tables["sow_chunks"]["name"]} AS {tables["sow_chunks"]["alias"]} ON {tables["sows"]["alias"]}.id = {tables["sow_chunks"]["alias"]}.sow_id'

        #if intent == 'performance' or intent == 'accuracy':
        #query += ' LEFT JOIN sow_validation_results AS v ON s.id = v.sow_id'

        #query = 'SELECT id, number, vendor_id, start_date, end_date, budget, document FROM sows'
        
        if vendor_id is not None:
            query += f' WHERE vendor_id = {vendor_id}'

        rows = await conn.fetch(f'{query};')
        sows = [dict(row) for row in rows]
    return sows

async def get_vendors():
    """Retrieves a list of vendors from the database."""
    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        query = 'SELECT * FROM vendors'
        #if name is not None:
        #   query += f" WHERE name = '{name}'"

        rows = await conn.fetch(f'{query};')
        vendors = [Vendor(**dict(row)) for row in rows]
    return vendors