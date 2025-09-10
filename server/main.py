from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv(dotenv_path="../.env")

API_KEY = os.environ.get("API_KEY")
GOOGLE_TRANSLATE_URL = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"

class TranslateRequest(BaseModel):
    text: str
    target: str = "zh"

@app.post("/translate")
def translate_text(req: TranslateRequest):
    print(API_KEY)
    data = {"q": req.text, "target": req.target}

    response = requests.post(GOOGLE_TRANSLATE_URL, data=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()
    translated_text = result["data"]["translations"][0]["translatedText"]
    detected_source = result["data"]["translations"][0].get("detectedSourceLanguage", "unknown")

    return {
        "input": req.text,
        "translatedText": translated_text,
        "detectedSourceLanguage": detected_source
    }
