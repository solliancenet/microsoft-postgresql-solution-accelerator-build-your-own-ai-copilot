from azure.identity.aio import DefaultAzureCredential
from azure.ai.formrecognizer.aio import DocumentAnalysisClient


class AzureDocIntelligenceService:
    def __init__(self, credential: DefaultAzureCredential, docIntelligenceEndpoint: str):
        self.credential = credential

        self.document_analysis_client = DocumentAnalysisClient(
            endpoint=docIntelligenceEndpoint,
            credential=DefaultAzureCredential()
        )

    async def extract_text_from_document(self, document_data):
        """Extract text and structure using Azure AI Document Intelligence."""
        poller = await self.document_analysis_client.begin_analyze_document(
            model_id="prebuilt-document",
            document=document_data
        )
        result = await poller.result()
        extracted_text = []
        for page in result.pages:
            page_text = " ".join([line.content for line in page.lines])
            extracted_text.append(page_text)
        return extracted_text
