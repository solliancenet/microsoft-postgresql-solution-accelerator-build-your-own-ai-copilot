from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer.aio import DocumentAnalysisClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from datetime import date, datetime
import re



class TextChunk:
    heading: str
    content: str
    page_number:int

class DocumentAnalysisResult:
    extracted_text: str
    text_chunks: List[TextChunk]


class InvoiceLineItem:
    description: str
    amount: str
    due_date: date
    status: str

class InvoiceDocumentAnalysisResult(DocumentAnalysisResult):
    line_items: List[InvoiceLineItem]


class AzureDocIntelligenceService:
    def __init__(self, credential: AzureKeyCredential, docIntelligenceEndpoint: str):
        self.credential = credential
        self.docIntelligenceEndpoint = docIntelligenceEndpoint

    async def extract_text_from_sow_document(self, document_data):
        """Extract text and structure using Azure AI Document Intelligence."""
        docClient = DocumentAnalysisClient(
            endpoint=self.docIntelligenceEndpoint,
            credential=self.credential
        )

        poller = await docClient.begin_analyze_document(
            model_id="prebuilt-document",
            document=document_data
        )

        result = await poller.result()

        analysis = DocumentAnalysisResult()
        analysis.extracted_text = []
        analysis.text_chunks = []
        
        known_headings = [
            "Project Scope", "Project Objectives", "Location", "Tasks", "Schedules",
            "Standards and Testing", "Payments", "Compliance", "Requirements", "Project Deliverables"
        ]

        for page in result.pages:
            page_text = " ".join([line.content for line in page.lines])
            analysis.extracted_text.append(page_text)

            current_heading = None
            for line in page.lines:
                text = line.content
                if self.__is_heading(text, known_headings): # Detect headings
                    current_heading = text
                    newTextChunk = TextChunk()
                    newTextChunk.heading = text
                    newTextChunk.content = ""
                    newTextChunk.page_number = page.page_number
                    analysis.text_chunks.append(newTextChunk)
                elif current_heading:
                    analysis.text_chunks[-1].content += " " + text

        await docClient.close()

        analysis.full_text = "\n".join(analysis.extracted_text)

        return analysis

    async def extract_text_from_invoice_document(self, document_data):
        """Extract text and structure using Azure AI Document Intelligence."""
        docClient = DocumentAnalysisClient(
            endpoint=self.docIntelligenceEndpoint,
            credential=self.credential
        )

        poller = await docClient.begin_analyze_document(
            model_id="prebuilt-invoice",
            document=document_data
        )

        result = await poller.result()

        analysis = InvoiceDocumentAnalysisResult()
        analysis.extracted_text = []
        analysis.text_chunks = []
        analysis.line_items = []
        
        for page in result.pages:
            page_text = " ".join([line.content for line in page.lines])
            analysis.extracted_text.append(page_text)

        invoiceDocument = result.documents[0] # Assuming a single invoice document
        items_field = invoiceDocument.fields.get("Items")
        if items_field and items_field.value:
            for item in items_field.value:
                line_item = InvoiceLineItem()

                description_field = item.value.get("Description")
                amount_field = item.value.get("Amount")
                due_date_field = item.value.get("Date")

                # Extract and clean up fields
                line_item.description = description_field.content if description_field else "N/A"
                line_item.amount = amount_field.content if amount_field else "0"
                
                # Remove currency symbols or extra characters from amount
                line_item.amount = float(re.sub(r"[^\d.]", "", line_item.amount))

                # Extract due date
                text_due_date = due_date_field.content if due_date_field else "1970-01-01"
                line_item.due_date = datetime.strptime(text_due_date, '%Y-%m-%d').date() if text_due_date else None

                # Determine the status based on the due date
                line_item.status = 'Completed' if line_item.due_date and line_item.due_date < date(2024, 12, 31) else 'Pending'  # Changed line

                analysis.line_items.append(line_item)
            

        await docClient.close()

        analysis.full_text = "\n".join(analysis.extracted_text)

        return analysis

    def __is_heading(self, text, known_headings):
        # Check if the text matches any known headings
        if text.strip() in known_headings:
            return True
        
        return False

    def semantic_chunking(self, text):
        """Chunk text into semantically meaningful pieces."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,         # Maximum characters per chunk
            chunk_overlap=50        # Overlap between chunks
        )
        return text_splitter.split_text(text)


    def extract_sow_metadata(self, full_text):
        """Extract SOW metadata"""
        metadata = {
            "content": full_text
        }

        # Extract SOW Number
        match = re.search(r'SOW Number:\s*(SOW-\S+)', full_text, re.IGNORECASE)
        if match:
            metadata['sow_number'] = match.group(1)
        else:
            metadata['sow_number'] = None

        return metadata

    def extract_invoice_metadata(self, full_text):
        """Extract invoice metadata such as number, amount, and invoice_date from text."""
        metadata = {}

        # Extract Vendor Name
        # match = re.search(r'Vendor:\s*([^\n]+)', full_text, re.IGNORECASE)
        # metadata['vendor'] = match.group(1).strip() if match else "UNKNOWN"

        # Extract invoice number
        #match = re.search(r"Invoice Number[:\s]+([A-Za-z0-9-]+)", full_text, re.IGNORECASE)
        match = re.search(r'Invoice Number:\s*(INV-\S+)', full_text, re.IGNORECASE)
        metadata['number'] = match.group(1) if match else "UNKNOWN"

        # Extract invoice amount
        match = re.search(r"Total Amount[:\s]+[$]?([\d,]+(?:\.\d{1,2})?)", full_text, re.IGNORECASE)
        metadata['amount'] = float(match.group(1).replace(",", "")) if match else 0.0

        # Extract invoice date
        match = re.search(r"Invoice Date[:\s]+([\d/-]{8,10})", full_text, re.IGNORECASE)
        if match:
            try:
                metadata['invoice_date'] = datetime.strptime(match.group(1), "%Y-%m-%d").date()
            except ValueError:
                metadata['invoice_date'] = None
        else:
            metadata['invoice_date'] = None

        # Extract SOW Number
        match = re.search(r'SOW Number:\s*(SOW-\S+)', full_text, re.IGNORECASE)
        if match:
            metadata['sow_number'] = match.group(1)
        else:
            metadata['sow_number'] = None

        # Default payment status
        metadata['payment_status'] = "Pending"

        return metadata