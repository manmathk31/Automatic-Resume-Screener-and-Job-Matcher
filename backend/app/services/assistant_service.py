import os
import google.generativeai as genai

try:
    from decouple import config
    api_key = config("GEMINI_API_KEY", default=None)
except ImportError:
    api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

def generate_assistant_response(query: str, context: str) -> str:
    # a) what the system prompt string looks like (built from context)
    system_prompt = (
        "You are an expert HR Assistant. Use the provided context to answer questions "
        "about candidate rankings and job matching.\n\n"
        f"Context:\n{context}"
    )
    
    # b) what the user message string looks like (the query)
    user_message = query
    
    # c) a comment block:
    # YOUR LLM CALL GOES HERE — see step 3
    if not api_key:
        return "Error: GEMINI_API_KEY is not configured in environment."
        
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=system_prompt
        )
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini API: {e}"
