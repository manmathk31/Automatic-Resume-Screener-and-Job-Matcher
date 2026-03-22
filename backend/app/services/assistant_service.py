import os
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

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
                max_output_tokens=4096,
            )
        )
        return response.text
    except Exception as e:
        error_str = str(e)
        logger.error(f"Gemini API error: {error_str}")
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            return "The AI assistant is temporarily busy due to high usage. Please wait a moment and try again."
        if "404" in error_str or "not found" in error_str.lower():
            return "AI model configuration error. Please contact support."
        if "API_KEY" in error_str or "401" in error_str:
            return "AI assistant is not configured correctly. Please contact support."
        return "The AI assistant is temporarily unavailable. Please try again in a moment."