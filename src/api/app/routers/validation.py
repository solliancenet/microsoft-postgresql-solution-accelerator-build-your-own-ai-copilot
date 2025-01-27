from datetime import datetime, timezone
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool

from datetime import date

from app.lifespan_manager import get_chat_client, get_db_connection_pool
from app.models import ValidationRequest, Invoice, Vendor, Sow, Milestone, Deliverable, InvoiceLineItem
from fastapi import APIRouter, Depends, HTTPException

from pydantic import parse_obj_as, BaseModel
from typing import Optional

class InvoiceModel(Invoice):
    vendor: Optional[Vendor] = None
    line_items: Optional[list[InvoiceLineItem]] = None
    
class SowModel(Sow):
    milestones: Optional[list[Milestone]] = None

class MilestoneModel(Milestone):
    deliverables: Optional[list[Deliverable]] = None



# Initialize the router
router = APIRouter(
    prefix = "/validation",
    tags = ["Validation"],
    dependencies = [Depends(get_chat_client)],
    responses = {404: {"description": "Not found"}}
)

@router.post('/invoice/{id}', response_model = str)
#async def validate_invoice_by_id(request: ValidationRequest, id: int, llm = Depends(get_chat_client)):
async def validate_invoice_by_id(id: int, llm = Depends(get_chat_client)):
    """Generate a chat completion to Validate the Invoice using the Azure OpenAI API."""
    # TODO: Move this system prompt into blob storage or somewhere it can be updated without redeploying the app.
    # Define the system prompt that contains the assistant's persona.
    system_prompt = f"""
    You are an intelligent copilot for Woodgrove Bank designed to automate the validation of vendor invoices against billing milestones in statements of work (SOWs).
   
    When validating an invoice, you should:
    1. Verify that the invoice number matches the vendor's records.
    2. Check that the total amount on the invoice is correct.
    3. Ensure that the milestone delivery dates are before or on the specified due date in the SOW.
    4. Assess any late fees or penalties that may apply, as defined by the SOW. For example, if a milestone is late, a penalty of 15% should be applied to payment of that milestone.
    5. Validate the line items on the invoice against the billing milestones in the SOW.
    6. Ensure that the amount billed for each line item matches the billable amount specified in the SOW.
    7. If the invoice contains notes to explain discrepancies, review them for additional context.
    8. Confirm that the invoice is legitimate and ready for payment.

    For context, today is {datetime.now(timezone.utc).strftime('%A, %B %d, %Y')}.

    If there are milestones missing from the invoice that are not yet beyond their due date according to the SOW, do not flag them as discrepancies.
    If the payment terms on the invoice are different from the SOW, assume the SOW is correct.

    In your response:
    - Provide a statement of valid or invalid for the invoice.
    - Create separate sections for the invoice and the milestone validation.
    - Provide a detailed summary of the validation results, including any discrepancies or anomalies found between the invoice and the SOW.
    - If any discrepancies or anomalies are found, you should provide detailed feedback on the issues discovered, like including dollar amounts, line items, and due dates.
    - If there are any discrepancies, flag the invoice for further review.

    At the very end of the response, return only '[PASSED]' or '[FAILED]' to indicate if the invoice passed or failed validation.
    """
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
    
    # TODO: Define tools for the agent
    tools = [
         StructuredTool.from_function(coroutine=validate_invoice)
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
async def validate_sow_by_id(id: int, llm = Depends(get_chat_client)):
    """Generate a chat completion to Validate the SOW using the Azure OpenAI API."""

    # Define the system prompt that contains the assistant's persona.
    system_prompt = f"""
    You are an intelligent copilot for Woodgrove Bank designed to automate the validation of vendor invoices against billing milestones in statements of work (SOWs).
   
    When validating a SOW, you should:
    1. Verify that the SOW number matches the vendor's records.
    2. Check that the total amount on the SOW is correct.
    3. Ensure that the milestone delivery dates are before or on the specified due date in the SOW.
    4. Assess any late fees or penalties that may apply, as defined by the SOW. For example, if a milestone is late, a penalty of 15% should be applied to payment of that milestone.
    5. Validate the deliverables for each milestone in the SOW.
    6. Ensure that the amount billed for each deliverable matches the billable amount specified in the SOW.
    7. If the SOW contains notes to explain discrepancies, review them for additional context.
    8. Confirm that the SOW is legitimate and ready for payment.

    For context, today is {datetime.now(timezone.utc).strftime('%A, %B %d, %Y')}.

    In your response:
    - Provide a statement of valid or invalid for the SOW.
    - Create separate sections for the SOW and the milestone validation.
    - Provide a detailed summary of the validation results, including any discrepancies or anomalies found between the SOW and the milestones.
    - If any discrepancies or anomalies are found, you should provide detailed feedback on the issues discovered, like including dollar amounts, line items, and due dates.
    - If there are any discrepancies, flag the SOW for further review.

    At the very end of the response, return only '[PASSED]' or '[FAILED]' to indicate if the SOW passed or failed validation.
    """
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

    # TODO: Define tools for the agent
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


