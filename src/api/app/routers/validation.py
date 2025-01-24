from datetime import datetime, timezone
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool

from datetime import date

from app.lifespan_manager import get_chat_client, get_db_connection_pool
from app.models import ValidationRequest
from fastapi import APIRouter, Depends

# Initialize the router
router = APIRouter(
    prefix = "/validation",
    tags = ["Validation"],
    dependencies = [Depends(get_chat_client)],
    responses = {404: {"description": "Not found"}}
)

@router.post('/validate_invoice/{id}', response_model = str)
async def validate_invoice_by_id(request: ValidationRequest, id: int, llm = Depends(get_chat_client)):
    """Generate a chat completion using the Azure OpenAI API."""
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
    """
    # Provide the validation copilot with a persona using the system prompt.
    messages = [{ "role": "system", "content": system_prompt }]

    # Add the current user message to the messages list
    messages.append({"role": "user", "content": request.message})

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
    completion = await agent_executor.ainvoke({"input": request.message})
    return completion['output']

async def validate_invoice(vendor: str, invoice_number: str):
    """Validates an invoice against billing milestones in an SOW."""

    # TODO: Look up invoice and SOW data from the database
    # Populate the invoice with data from the database
    invoice = Invoice(
        #vendor = Vendor(name=vendor),
        number = invoice_number,
        total_amount = 12500.00,
        date = date(2024, 12, 30),
        line_items = [
            InvoiceLineItem(description="Copilot solution accelerator development", amount=10001.00),
            InvoiceLineItem(description="Solution testing", amount=2500.00)
        ],
        payment_terms = "Net 10",
        notes = "Late fee not applied, per secondary agreement to deliver testing at the same time as accelerator solution."
    )

    # Get a collection of the billing milestones from the SOW.
    sow = StatementOfWork(
        number = "SOW-2024-001",
        milestones = [
            Milestone(
                number = 1,
                name = "Copilot solution accelerator development",
                deliverables = ["Copilot solution accelerator development"],
                billable_amount = 14400.00,
                amount_paid = 7200.00,
                due_date = date(2024, 12, 31)
            ),
            Milestone(
                number = 2,
                name = "Solution testing",
                deliverables = ["Solution testing"],
                billable_amount = 2500.00,
                amount_paid = 0.00,
                due_date = date(2024, 12, 20)
            ),
            Milestone(
                number = 3,
                name = "Solution documentation",
                deliverables = ["Documentation"],
                billable_amount = 4000.00,
                amount_paid = 0.00,
                due_date = date(2025, 1, 31)
            ),
            Milestone(
                number = 4,
                name = "Onsite training",
                deliverables = ["Travel", "Training"],
                billable_amount = 4500.00,
                amount_paid = 0.00, 
                due_date = date(2025, 2, 28)
            )
        ],
        payment_terms = "Net 30",
        late_delivery_penalty = 0.10
    )

    return invoice, sow

from pydantic import BaseModel
from typing import Optional

class Milestone(BaseModel):
    number: int
    name: str
    deliverables: list[str]
    billable_amount: float
    amount_paid: float
    due_date: date

class StatementOfWork(BaseModel):
    number: str
    milestones: list[Milestone]
    payment_terms: str
    late_delivery_penalty: float = 0.10

class InvoiceLineItem(BaseModel):
    description: str
    amount: float

class Invoice(BaseModel):
    #vendor: Vendor
    number: str
    total_amount: float
    date: date
    line_items: list[InvoiceLineItem]
    payment_terms: str
    notes: Optional[str] = None
