import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
load_dotenv()

FORM_ENDPOINT = os.getenv("AZURE_FORM_ENDPOINT")
FORM_KEY = os.getenv("AZURE_FORM_KEY")

def _init_client():
    if not FORM_ENDPOINT or not FORM_KEY:
        raise EnvironmentError("AZURE_FORM_ENDPOINT and AZURE_FORM_KEY must be set in env")
    return DocumentAnalysisClient(FORM_ENDPOINT, AzureKeyCredential(FORM_KEY))

def analyze_document(file_bytes: bytes):
    """
    Analyze document using prebuilt 'document' model.
    Returns dict: { "text": "...", "fields": { ... } }
    """
    client = _init_client()
    poller = client.begin_analyze_document("prebuilt-document", document=file_bytes)
    result = poller.result()
    # extract plain text from pages/lines
    text_blocks = []
    for page in result.pages:
        for line in page.lines:
            text_blocks.append(line.content)
    full_text = "\n".join(text_blocks).strip()
    # try to extract key/value pairs from result.documents or keyValuePairs if present
    fields = {}
    try:
        if result.documents:
            for doc in result.documents:
                for name, field in doc.fields.items():
                    fields[name] = field.value if getattr(field, 'value', None) is not None else str(getattr(field, 'content', ''))
    except Exception:
        pass
    # as fallback, try keyValuePairs
    try:
        if hasattr(result, "key_value_pairs"):
            for kv in result.key_value_pairs:
                k = kv.key.content if kv.key else None
                v = kv.value.content if kv.value else None
                if k:
                    fields[k] = v
    except Exception:
        pass
    return {"text": full_text, "fields": fields}
