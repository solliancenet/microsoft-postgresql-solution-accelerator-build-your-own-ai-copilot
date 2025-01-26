from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer.aio import DocumentAnalysisClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

class DocumentAnalysisResult:
    extracted_text: str
    full_text: str
    text_chunks: List[str]

class AzureDocIntelligenceService:
    def __init__(self, credential: AzureKeyCredential, docIntelligenceEndpoint: str):
        self.credential = credential
        self.docIntelligenceEndpoint = docIntelligenceEndpoint

    async def close(self):
        await self.document_analysis_client.close()

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
        extracted_text = []
        
        for page in result.pages:
            page_text = " ".join([line.content for line in page.lines])
            extracted_text.append(page_text)

        docClient.close()

        return extracted_text

    def semantic_chunking(self, text):
        """Chunk text into semantically meaningful pieces."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,         # Maximum characters per chunk
            chunk_overlap=50        # Overlap between chunks
        )
        return text_splitter.split_text(text)