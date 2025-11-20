from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from typing import List, Optional
from logger import setup_logging

log = setup_logging(ci_mode=False)
SUMO_ENDPOINT = os.getenv("SUMO_ENDPOINT")
class SumoLogicHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        try:
            requests.post(SUMO_ENDPOINT, data=log_entry.encode("utf-8"))
        except Exception:
            pass  # don't crash app on logging failure

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging(ci_mode=False):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG if ci_mode else logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if not ci_mode:
        file_handler = RotatingFileHandler(
            f"{LOG_DIR}/server.log",
            maxBytes=5_000_000,
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    sumo_handler = SumoLogicHandler()
    sumo_handler.setFormatter(formatter)
    logger.addHandler(sumo_handler)
    
    return logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://csci-40500-fall-2025.github.io/project-megatron/","https://csci-40500-fall-2025.github.io"],
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
    verbs: Optional[List[str]] = None


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str

USERS = {}

@app.post("/signup")
def signup(req: SignUpRequest):
    email = req.email.lower()
    password = req.password

    # validate password
    ok, errors = is_strong_password(password)
    if not ok:
        raise HTTPException(status_code=400, detail={"errors": errors})

    # check for existing user
    if email in USERS:
        raise HTTPException(status_code=409, detail="User already exists")

    # hashed = hash_password(password)
    USERS[email] = {
        "email": email,
        "password": password,
        "created_at": datetime.utcnow().isoformat(),
    }

    return {"email": email, "created_at": USERS[email]["created_at"]}

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
        "translatedNouns": noun_translations,
        "translatedVerbs": verb_translations
    }

def is_valid_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    return bool(re.match(r"^\S+@\S+\.\S+$", email))


def is_strong_password(password: str) -> Tuple[bool, list]:
    errors = []
    if not isinstance(password, str):
        errors.append("password must be a string")
        return False, errors
    if len(password) < 12:
        errors.append("password must be at least 12 characters")
    if not re.search(r"\d", password):
        errors.append("password must contain a number")
    if not re.search(r"[^A-Za-z0-9]", password):
        errors.append("password must contain a special character")
    return len(errors) == 0, errors