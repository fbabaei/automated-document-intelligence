# Automated Document Intelligence System (ADIS)

This project is a Streamlit demo that uses **Azure Document Intelligence (Form Recognizer)** to extract text/fields from uploaded documents, and **OpenAI** to generate concise summaries.

## Features
- Upload PDF / JPG / PNG files
- Extract plain text and structured fields with Azure Document Intelligence (prebuilt document model)
- Generate bullet-point summaries using OpenAI ChatCompletion
- Ready to deploy on Streamlit Cloud or other hosting

## Setup (Local)
1. Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file (or set environment variables). See `.env.example` for template.
```
AZURE_FORM_ENDPOINT=https://<your-form-recognizer-endpoint>.cognitiveservices.azure.com/
AZURE_FORM_KEY=<your-form-recognizer-key>
OPENAI_API_KEY=<your-openai-api-key>
```

4. Run the app:
```bash
streamlit run app.py
```

## Deploy to Streamlit Cloud
- Push this repo to GitHub.
- Go to https://share.streamlit.io and connect your repo.
- In Streamlit Cloud settings, add the following Secrets: `AZURE_FORM_ENDPOINT`, `AZURE_FORM_KEY`, `OPENAI_API_KEY`.
- Deploy; the app will be publicly accessible.

## Notes & Security
- Do **not** commit your keys to source control. Use environment variables / Streamlit Secrets.
- If your documents contain sensitive PII, evaluate whether it is acceptable to send content to OpenAI. Consider masking or using an on-premise model for sensitive data.
