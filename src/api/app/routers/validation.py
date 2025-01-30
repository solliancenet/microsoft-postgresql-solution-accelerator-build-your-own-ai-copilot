from datetime import datetime, timezone
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from app.lifespan_manager import get_chat_client, get_db_connection_pool, get_prompt_service
from app.models import ValidationRequest, Vendor, Milestone, Deliverable, InvoiceLineItem
from fastapi import APIRouter, Depends, HTTPException
from app.models.validation import InvoiceModel, SowModel, MilestoneModel
from datetime import date
from pydantic import parse_obj_as

# Initialize the router
router = APIRouter(
    prefix = "/validation",
    tags = ["Validation"],
    dependencies = [Depends(get_chat_client)],
    responses = {404: {"description": "Not found"}}
)

@router.post('/invoice/{id}', response_model = str)
#async def validate_invoice_by_id(request: ValidationRequest, id: int, llm = Depends(get_chat_client)):
async def validate_invoice_by_id(id: int, llm = Depends(get_chat_client), prompt_service = Depends(get_prompt_service)):
    """Generate a chat completion to Validate the Invoice using the Azure OpenAI API."""
    
    # Define the system prompt for the validator.
    system_prompt = prompt_service.get_prompt("invoice_validation")
    # Append the current date to the system prompt to provide context when checking timeliness of deliverables.
    system_prompt += f"\n\nFor context, today is {datetime.now(timezone.utc).strftime('%A, %B %d, %Y')}."

    # Provide the validation copilot with a persona using the system prompt.
    messages = [{ "role": "system", "content": system_prompt }]

    # Add the current user message to the messages list
    userMessage = f"""validate Invoice with ID of {id}"""
    messages.append({"role": "user", "content": userMessage})

    # Create a chat prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ]
    )
    
    # Define tools for the agent
    tools = [
         StructuredTool.from_function(coroutine=validate_invoice)
    ]
    
    # Create an AI agent
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

    # Invoke the agent to perform a chat completion that provides the validation results.
    completion = await agent_executor.ainvoke({"input": userMessage})
    validationResult = completion['output']

    # Check if validationResult contains [PASSED] or [FAILED]
    # This is based on the prompt telling the AI to return either [PASSED] or [FAILED]
    # at the end of the response to indicate if the invoice passed or failed validation.
    validation_passed = validationResult.find('[PASSED]') != -1

    # Write validation result to database
    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        await conn.execute('''
        INSERT INTO invoice_validation_results (invoice_id, datestamp, result, validation_passed)
        VALUES ($1, $2, $3, $4);
        ''', id, datetime.utcnow(), validationResult, validation_passed)

    return validationResult

async def validate_invoice(id: int):
    """Retrieves an Invoice and it's associated Line Items, SOW, and Milestones."""

    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM invoices WHERE id = $1;', id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'An invoice with an id of {id} was not found.')
        invoice = parse_obj_as(InvoiceModel, dict(row))

        # Get the vendor name
        vendor_row = await conn.fetchrow('SELECT * FROM vendors WHERE id = $1;', invoice.vendor_id)
        invoice.vendor = parse_obj_as(Vendor, dict(vendor_row))

        # Get the invoice line items
        line_item_rows = await conn.fetch('SELECT * FROM invoice_line_items WHERE invoice_id = $1;', id)
        invoice.line_items = [parse_obj_as(InvoiceLineItem, dict(row)) for row in line_item_rows]



        # Get the SOW
        sow_row = await conn.fetchrow('SELECT * FROM sows WHERE id = $1;', invoice.sow_id)
        sow = parse_obj_as(SowModel, dict(sow_row))

        # Get the milestones
        milestone_rows = await conn.fetch('SELECT * FROM milestones WHERE sow_id = $1;', invoice.sow_id)
        sow.milestones = [parse_obj_as(MilestoneModel, dict(row)) for row in milestone_rows]

        # Get the deliverables for each milestone
        for milestone in sow.milestones:
            deliverable_rows = await conn.fetch('SELECT * FROM deliverables WHERE milestone_id = $1;', milestone.id)
            milestone.deliverables = parse_obj_as(list[Deliverable], [dict(row) for row in deliverable_rows])
       

    return invoice, sow


@router.post('/sow/{id}', response_model = str)
async def validate_sow_by_id(id: int, llm = Depends(get_chat_client), prompt_service = Depends(get_prompt_service)):
    """Generate a chat completion to Validate the SOW using the Azure OpenAI API."""

    # Define the system prompt for the validator.
    system_prompt = prompt_service.get_prompt("sow_validation")
    # Append the current date to the system prompt to provide context when checking timeliness of deliverables.
    system_prompt += f"\n\nFor context, today is {datetime.now(timezone.utc).strftime('%A, %B %d, %Y')}."

    # Provide the validation copilot with a persona using the system prompt.
    messages = [{ "role": "system", "content": system_prompt }]

    # Add the current user message to the messages list
    userMessage = f"""validate SOW with ID {id}"""
    messages.append({"role": "user", "content": userMessage})

    # Create a chat prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ]
    )

    tools = [
         StructuredTool.from_function(coroutine=validate_sow)
    ]
    
    # Create an agent
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)
    #completion = await agent_executor.ainvoke({"input": request.message})
    completion = await agent_executor.ainvoke({"input": userMessage})

    validationResult = completion['output']

    # Check if validationResult contains [PASSED] or [FAILED]
    validation_passed = validationResult.find('[PASSED]') != -1

    # Write validation result to database
    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        await conn.execute('''
        INSERT INTO sow_validation_results (sow_id, datestamp, result, validation_passed)
        VALUES ($1, $2, $3, $4);
        ''', id, datetime.utcnow(), validationResult, validation_passed)

    return validationResult

async def validate_sow(id: int):
    """Retrieves a SOW and it's associated Milestones and Deliverables."""

    pool = await get_db_connection_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM sows WHERE id = $1;', id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A SOW with an id of {id} was not found.')
        sow = parse_obj_as(SowModel, dict(row))

        # Get the milestones
        milestone_rows = await conn.fetch('SELECT * FROM milestones WHERE sow_id = $1;', id)
        sow.milestones = [parse_obj_as(MilestoneModel, dict(row)) for row in milestone_rows]

        # Get the deliverables for each milestone
        for milestone in sow.milestones:
            deliverable_rows = await conn.fetch('SELECT * FROM deliverables WHERE milestone_id = $1;', milestone.id)
            milestone.deliverables = parse_obj_as(list[Deliverable], [dict(row) for row in deliverable_rows])

    return sow


