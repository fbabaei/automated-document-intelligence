import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import os

st.set_page_config(page_title="📄 Automated Document Intelligence", layout="wide")
st.title("📄 Automated Document Intelligence System")

# --- Load secrets from Hugging Face ---
AZURE_FORM_ENDPOINT = os.getenv("AZURE_FORM_ENDPOINT")
AZURE_FORM_KEY = os.getenv("AZURE_FORM_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

# --- Verify credentials ---
if not all([AZURE_FORM_ENDPOINT, AZURE_FORM_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY]):
    st.error("⚠️ Missing Azure credentials. Please set environment variables in Hugging Face Space secrets.")
    st.stop()

# --- Initialize clients ---
form_client = DocumentAnalysisClient(endpoint=AZURE_FORM_ENDPOINT, credential=AzureKeyCredential(AZURE_FORM_KEY))
openai_client = AzureOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_KEY, api_version="2024-02-01")

# --- File uploader ---
uploaded_file = st.file_uploader("Upload a document (PDF, JPG, PNG)", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file:
    st.write("Analyzing document with Azure Form Recognizer...")
    poller = form_client.begin_analyze_document("prebuilt-document", document=uploaded_file)
    result = poller.result()

    extracted_text = ""
    for page in result.pages:
        for line in page.lines:
            extracted_text += line.content + "\n"

    st.subheader("📑 Extracted Text")
    st.text_area("Extracted content", extracted_text, height=250)

    if st.button("Summarize with Azure OpenAI"):
        with st.spinner("Generating summary..."):
            response = openai_client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": "You are an expert summarizer."},
                    {"role": "user", "content": f"Summarize this document:\n{extracted_text}"}
                ]
            )
            summary = response.choices[0].message.content
            st.success("✅ Summary generated!")
            st.text_area("Summary", summary, height=200)
