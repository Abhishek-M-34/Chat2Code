import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_frontend_code(user_prompt, current_html=None):
    
    system_instruction = """
    You are an expert Full-Stack AI Web Developer.
    
    YOUR GOAL:
    Create highly visual, interactive single-page websites based on user requests.
    
    CRITICAL INSTRUCTION FOR OUTPUT:
    - Output a SINGLE 'index.html' string.
    - EMBED CSS inside <style> tags.
    - EMBED JS inside <script> tags.
    - Use CDNs for libraries (Tailwind, React, Three.js, Anime.js).
    
    SCENARIO HANDLING:
    - If user asks for "Obsidian Graph": Use <script src="https://unpkg.com/force-graph"></script>.
    - If user asks for "3D": Use Three.js.
    - If user asks for "Modern UI": Use Tailwind CSS.
    
    OUTPUT FORMAT (Strict JSON):
    {
      "message": "I built a physics-based graph view for you.",
      "html": "<!DOCTYPE html><html lang='en'><head>...</head><body>...</body></html>"
    }
    """

    messages = [{"role": "system", "content": system_instruction}]
    
    # Pass previous code context so AI can edit it
    if current_html:
        messages.append({
            "role": "user", 
            "content": f"CURRENT CODE:\n{current_html}\n\nUSER REQUEST: {user_prompt}"
        })
    else:
        messages.append({
            "role": "user", 
            "content": f"Create a new website. REQUEST: '{user_prompt}'"
        })

    try:
        completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return json.loads(completion.choices[0].message.content)
    
    except Exception as e:
        print(f"AI Error: {e}")
        return {
            "message": "I encountered an error generating the code.",
            "html": current_html or "<h1>Error</h1>"
        }