from pathlib import Path
from config import GOOGLE_AI_STUDIO_API_FILE

# from plugins.gepeto.plugin import gepeto
# print(gepeto("What is your model?"))

def get_gemini_api_key():
    key_file = open(f"{Path.home()}/{GOOGLE_AI_STUDIO_API_FILE}", "r")
    api_key = key_file.read()
    key_file.close()
    return api_key.strip()


from google import genai

client = genai.Client(api_key=get_gemini_api_key())


def gepeto(q: str) -> str:
    response = client.models.generate_content(model="gemini-2.0-flash", contents=q)
    return response
