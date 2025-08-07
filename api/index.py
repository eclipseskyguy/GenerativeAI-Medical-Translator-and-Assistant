# api/index.py

import os
import io
import logging
import google.generativeai as genai
import json
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from gtts import gTTS
from googletrans import Translator

# --- Configuration ---
app = FastAPI()
templates = Jinja2Templates(directory="templates")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logging.warning("GEMINI_API_KEY not found. AI features will be disabled.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Models ---
class APIRequest(BaseModel):
    text: str
    lang_code: str

class AIRequest(BaseModel):
    text: str
    original_lang: str
    target_lang: str

# --- Frontend Endpoint ---
@app.get("/")
async def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- API Endpoints ---
@app.post("/translate/")
async def translate_text_only(text: str = Form(...), input_lang_code: str = Form(...), output_lang_code: str = Form(...)):
    try:
        translator = Translator()
        translated_text = translator.translate(text, src=input_lang_code, dest=output_lang_code).text
        return { "original_text": text, "translated_text": translated_text, "original_lang_code": input_lang_code, "output_lang_code": output_lang_code }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech/")
async def generate_speech(request: APIRequest):
    try:
        tts = gTTS(request.text, lang=request.lang_code)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return StreamingResponse(mp3_fp, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
# --- UPDATED BILINGUAL AI ENDPOINTS ---
@app.post("/summarize/")
async def summarize_text(request: AIRequest):
    if not GEMINI_API_KEY: raise HTTPException(status_code=503, detail="AI feature not configured.")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        1. Summarize the following text in {request.target_lang}: '{request.text}'
        2. Translate that summary into {request.original_lang}.
        Provide a JSON object with two keys: 'summary_target_lang' and 'summary_original_lang'.
        """
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(response_mime_type="application/json"))
        return JSONResponse(content=json.loads(response.text))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI model failed: {str(e)}")

@app.post("/explain-medication/")
async def explain_medication(request: AIRequest):
    if not GEMINI_API_KEY: raise HTTPException(status_code=503, detail="AI feature not configured.")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        You are a friendly pharmacist. A patient has this text: '{request.text}'.
        1. Identify the primary medication. In {request.target_lang}, explain its purpose and common side effects in simple terms.
        2. Translate your explanation into {request.original_lang}.
        Provide a JSON object with two keys: 'explanation_target_lang' and 'explanation_original_lang'.
        """
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(response_mime_type="application/json"))
        return JSONResponse(content=json.loads(response.text))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI model failed: {str(e)}")