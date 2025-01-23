from azure.identity.aio import DefaultAzureCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


class AzureDocIntelligenceService:
    def __init__(self, credential: DefaultAzureCredential, docIntelligenceEndpoint: str):
        self.credential = credential

        self.document_analysis_client = DocumentAnalysisClient(
            endpoint=docIntelligenceEndpoint,
            credential=DefaultAzureCredential()
        )

    def extract_text_from_document(document_data):
        """Extract text and structure using Azure AI Document Intelligence."""
        poller = document_analysis_client.begin_analyze_document(
            model_id="prebuilt-document",
            document=document_data
        )
        result = poller.result()
        extracted_text = []
        for page in result.pages:
            page_text = " ".join([line.content for line in page.lines])
            extracted_text.append(page_text)
        return extracted_text
