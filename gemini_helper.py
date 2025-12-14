import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def translate_to_kannada(text: str) -> str:
    prompt = f"""
Translate the following agricultural pest advisory into simple Kannada
that a farmer can understand:

{text}
"""
    try:
        res = model.generate_content(prompt)
        return res.text.strip()
    except Exception:
        return text  # fallback
