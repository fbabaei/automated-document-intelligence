import os
import openai
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY must be set in env")
openai.api_key = OPENAI_API_KEY

def summarize_text(text: str, max_tokens: int = 300) -> str:
    """Call OpenAI ChatCompletion to produce a concise summary in bullet points."""
    if not text or text.strip() == "":
        return "No text to summarize."
    # truncate long text to stay within token limits for prompt
    prompt_text = text if len(text) < 15000 else text[:15000]
    messages = [
        {"role": "system", "content": "You are an assistant that summarizes documents into concise bullet point summaries. Focus on key facts, actions, entities, dates, and numeric values."},
        {"role": "user", "content": f"Summarize the following document in 8-12 concise bullet points:\n\n{prompt_text}"}
    ]
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.0
    )
    # handle response structure
    if "choices" in resp and len(resp["choices"])>0:
        content = resp["choices"][0]["message"]["content"]
        return content.strip()
    return ""
