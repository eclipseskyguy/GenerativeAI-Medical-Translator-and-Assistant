import os
import io
import logging
import google.generativeai as genai
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from gtts import gTTS
from googletrans import Translator

# --- Configuration ---
app = FastAPI()
templates = Jinja2Templates(directory="templates")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logging.warning("GEMINI_API_KEY not found. Summarization will be disabled.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Models ---
class TTSRequest(BaseModel):
    text: str
    lang_code: str

class SummarizeRequest(BaseModel):
    text: str

# --- Frontend Endpoint ---
@app.get("/")
async def serve_frontend(request: Request):
    """Serves the main HTML user interface."""
    return templates.TemplateResponse("index.html", {"request": request})

# --- API Endpoints ---
@app.post("/translate/")
async def translate_text_only(text: str = Form(...), input_lang_code: str = Form(...), output_lang_code: str = Form(...)):
    try:
        translator = Translator()
        translated_text = translator.translate(text, src=input_lang_code, dest=output_lang_code).text
        return { "original_text": text, "translated_text": translated_text, "output_lang_code": output_lang_code }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech/")
async def generate_speech(request: TTSRequest):
    try:
        tts = gTTS(request.text, lang=request.lang_code)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return StreamingResponse(mp3_fp, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize/")
async def summarize_text(request: SummarizeRequest):
    if not GEMINI_API_KEY: raise HTTPException(status_code=503, detail="AI Summarization feature is not configured.")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"You are a helpful medical assistant. Summarize the following text clearly and concisely in one simple sentence: '{request.text}'"
        response = model.generate_content(prompt)
        return {"summary": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI model failed: {str(e)}")