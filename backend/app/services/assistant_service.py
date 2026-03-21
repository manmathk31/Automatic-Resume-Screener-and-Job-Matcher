import os
from google import genai
from google.genai import types

try:
    from decouple import config
    api_key = config("GEMINI_API_KEY", default=None)
except ImportError:
    api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None

def generate_assistant_response(query: str, context: str) -> str:
    if not client:
        return "Error: GEMINI_API_KEY is not configured."

    system_prompt = (
        "You are an expert HR Assistant. Use the provided context to answer "
        "questions about candidate rankings and job matching.\n\n"
        f"Context:\n{context}"
    )

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=1024,
            )
        )
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini API: {e}"