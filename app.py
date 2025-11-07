import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  # Loads .env variables into os.environ

AZURE_FORM_ENDPOINT = os.getenv("AZURE_FORM_ENDPOINT")
AZURE_FORM_KEY = os.getenv("AZURE_FORM_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

# Validate environment variables
if not AZURE_FORM_KEY or not AZURE_FORM_ENDPOINT:
    raise ValueError("Please set AZURE_FORM_KEY and AZURE_FORM_ENDPOINT environment variables.")

if not AZURE_OPENAI_KEY or not AZURE_OPENAI_ENDPOINT:
    raise ValueError("Please set AZURE_OPENAI_KEY and AZURE_OPENAI_ENDPOINT environment variables.")

# Initialize clients
# form_client = DocumentAnalysisClient(endpoint=AZURE_FORM_ENDPOINT, credential=AzureKeyCredential(AZURE_FORM_KEY))
# openai_client = AzureOpenAI(
#     endpoint=AZURE_OPENAI_ENDPOINT,
#     api_key=AZURE_OPENAI_KEY,
#     api_version="2024-02-01"
# )
from openai import AzureOpenAI

config = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version="2023-12-01-preview"
)

client = AzureOpenAI(configuration=config)

st.set_page_config(page_title="Automated Document Intelligence", layout="wide")
st.title("📄 Automated Document Intelligence System")

uploaded_file = st.file_uploader("Upload a document (PDF, image)", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file:
    st.write("Processing document...")
    poller = form_client.begin_analyze_document("prebuilt-document", document=uploaded_file)
    result = poller.result()

    extracted_text = ""
    for page in result.pages:
        for line in page.lines:
            extracted_text += line.content + "\n"

    st.subheader("📑 Extracted Text")
    st.text_area("Document Content", extracted_text, height=250)

    if st.button("Summarize with Azure OpenAI"):
        with st.spinner("Generating summary..."):
            completion = openai_client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": "You are an AI that summarizes documents."},
                    {"role": "user", "content": f"Summarize this document:\n{extracted_text}"}
                ]
            )
            summary = completion.choices[0].message.get("content", "")
            st.success("✅ Summary generated!")
            st.text_area("Summary", summary, height=200)

