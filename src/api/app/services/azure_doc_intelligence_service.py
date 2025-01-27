from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer.aio import DocumentAnalysisClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from datetime import datetime
import re



class TextChunk:
    heading: str
    content: str
    page_number:int

class DocumentAnalysisResult:
    extracted_text: str
    text_chunks: List[TextChunk]


class AzureDocIntelligenceService:
    def __init__(self, credential: AzureKeyCredential, docIntelligenceEndpoint: str):
        self.credential = credential
        self.docIntelligenceEndpoint = docIntelligenceEndpoint

    async def extract_text_from_document(self, document_data):
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

        analysis = DocumentAnalysisResult(
            extracted_text=[],
            text_chunks=[]
        )
        
        known_headings = [
            "Project Scope", "Project Objectives", "Location", "Tasks", "Schedules",
            "Standards and Testing", "Payments", "Compliance", "Requirements", "Project Deliverables"
        ]

        for page in result.pages:
            page_text = " ".join([line.content for line in page.lines])
            analysis.extracted_text.append(page_text)

            for line in pages.lines:
                text = line.content
                if self.__is_heading(text, known_headings): # Detect headings
                    current_heading = text
                    analysis.text_chunks.append(TextChunk(heading=text, content="", page_number=page.page_number))
                elif current_heading:
                    analysis.text_chunks[-1].content += " " + text

        await docClient.close()

        analysis.full_text = "\n".join(analysis.extracted_text)

        return analysis

    def __is_heading(text, known_headings):
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

        # Extract invoice number
        match = re.search(r"Invoice Number[:\s]+([A-Za-z0-9-]+)", full_text, re.IGNORECASE)
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