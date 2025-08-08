# api/index.py

import os
import io
import logging
import json
import httpx
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from gtts import gTTS
from googletrans import Translator
import google.generativeai as genai

# --- Configuration ---
app = FastAPI()
templates = Jinja2Templates(directory="templates")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Models ---
class APIRequest(BaseModel):
    text: str
    lang_code: str = "en"

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

@app.post("/summarize/")
async def summarize_text(request: AIRequest):
    if not GEMINI_API_KEY: raise HTTPException(status_code=503, detail="AI feature not configured.")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"1. Summarize this in {request.target_lang}: '{request.text}'\n2. Translate the summary to {request.original_lang}.\nProvide JSON with keys 'summary_target_lang' and 'summary_original_lang'."
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(response_mime_type="application/json"))
        return JSONResponse(content=json.loads(response.text))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI model failed: {str(e)}")

@app.post("/explain-medication/")
async def explain_medication(request: AIRequest):
    if not GEMINI_API_KEY: raise HTTPException(status_code=503, detail="AI feature not configured.")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"You are a pharmacist. A patient has this text: '{request.text}'.\n1. In {request.target_lang}, identify the main medication and explain its purpose and side effects simply.\n2. Translate your explanation to {request.original_lang}.\nProvide JSON with keys 'explanation_target_lang' and 'explanation_original_lang'."
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(response_mime_type="application/json"))
        return JSONResponse(content=json.loads(response.text))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI model failed: {str(e)}")

# --- NEW: SIGN LANGUAGE FEATURE ENDPOINT ---
@app.post("/generate-sign-language/")
async def generate_sign_language(request: APIRequest):
    """
    Looks up words in an ASL dictionary API and returns video URLs.
    This is a prototype and works best for English.
    """
    # Sanitize and split text into words, removing punctuation
    words = ''.join(c for c in request.text if c.isalnum() or c.isspace()).lower().split()
    video_urls = []
    
    async with httpx.AsyncClient() as client:
        for word in words:
            if not word: continue
            try:
                # Using a free, public sign language dictionary API
                api_url = f"https://sign-language-api.vercel.app/api/v1/signs/search?query={word}"
                response = await client.get(api_url, timeout=10.0)
                if response.status_code == 200 and response.json():
                    # Find a result with a video URL
                    video_found = False
                    for sign in response.json():
                        if sign.get("videos") and sign["videos"][0].get("url"):
                             video_urls.append({"word": word, "url": sign["videos"][0]["url"]})
                             video_found = True
                             break # Use the first video found
                    if not video_found:
                        video_urls.append({"word": word, "url": None})
                else:
                    video_urls.append({"word": word, "url": None})
            except Exception as e:
                logging.error(f"Error fetching sign for '{word}': {e}")
                video_urls.append({"word": word, "url": None})

    return {"signs": video_urls}