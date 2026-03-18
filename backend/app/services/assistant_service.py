def generate_assistant_response(query: str, context: str) -> str:
    \"\"\"
    Mock for LLM response generation in HR Assistant.
    In reality, use OpenAI, Anthropic, or an open-source LLM.
    \"\"\"
    query_lower = query.lower()
    
    if "top candidates" in query_lower:
        return f"Based on the screening results, here are the top candidates context: {context}\nThey match closely with Python and ML requirements."
    elif "why" in query_lower and "ranked first" in query_lower:
        return f"The top candidate ranks highest because they match core requirements. Context details: {context}"
    elif "missing" in query_lower:
        return f"The most commonly missing skill among top candidates is Cloud Deployment. Context: {context}"
    
    return f"Assistant analyzed your query '{query}' against current database records. Found context: {context}"
