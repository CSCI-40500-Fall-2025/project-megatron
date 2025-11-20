from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from typing import List, Optional
from logger import setup_logging

log = setup_logging(ci_mode=False)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv(dotenv_path="../.env")

API_KEY = os.environ.get("API_KEY")
GOOGLE_TRANSLATE_URL = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"

class TranslateRequest(BaseModel):
    text: str
    target: str = "zh"
    nouns: Optional[List[str]] = None

@app.post("/translate")
def translate_text(req: TranslateRequest):
    log.info(f"Translation Requested: '{req.text}' → {req.target}")

    if not API_KEY:
        log.critical("Missing Google API Key!")
        raise HTTPException(status_code=500, detail="Server missing API key.")
    
    log.debug("Sending request to Google Translate API...")
    data = {"q": req.text, "target": req.target}

    response = requests.post(GOOGLE_TRANSLATE_URL, data=data)

    if response.status_code != 200:
        log.error(f"Google API error: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)

    log.debug("Received successful response from Google Translate API")
    result = response.json()
    translated_text = result["data"]["translations"][0]["translatedText"]
    detected_source = result["data"]["translations"][0].get("detectedSourceLanguage", "unknown")

    log.info(f"Translated text: '{translated_text}'")
    noun_translations = []
    if req.nouns:
        log.debug(f"Translating {len(req.nouns)} nouns...")
        for noun in req.nouns:
            log.info(f"Translation: {noun}")
            noun_data = {"q": noun, "target": req.target}
            noun_response = requests.post(GOOGLE_TRANSLATE_URL, noun_data)
            if noun_response.status_code != 200:
                log.warning(f"Failed to translate: '{noun}'")
                raise HTTPException(status_code=response.status_code, detail=response.text)
            else:
                noun_res = noun_response.json()
                t = noun_res["data"]["translations"][0]["translatedText"]
                noun_translations.append({"original": noun, "translated": t})
    log.info("Translation request completed successfully.") 
    return {
        "input": req.text,
        "translatedText": translated_text,
        "detectedSourceLanguage": detected_source,
        "translatedNouns": noun_translations
    }
