from google import genai

client = genai.Client()

def translate_to_kannada(text: str):
    if not text:
        return text

    prompt = f"""
    Translate the following agricultural advisory into simple farmer-friendly Kannada.
    Keep technical accuracy.
    
    Text:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text.strip()
