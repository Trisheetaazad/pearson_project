import os
from groq import Groq
import google.generativeai as genai
import os
from app.learning.feedback import get_learning_examples

def generate_summary(context, user_query, provider="gemini"):
    # Retrieve past human edits to train the model
    examples = get_learning_examples(limit=3)
    
    prompt = f"""
    You are an expert legal assistant. 
    
    REFERENCE EXAMPLES OF PREVIOUS EDITS:
    {examples}

    NEW CASE CONTEXT:
    {context}

    TASK:
    {user_query}
    """
    
    if provider.lower() == "gemini":
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL") or "gemini-1.5-flash")
        return model.generate_content(prompt).text
        
    elif provider.lower() == "groq":
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL") or "llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2 # Lower temperature for consistency
        )
        return response.choices[0].message.content