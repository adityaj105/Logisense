import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

app = FastAPI(title="LogiSense Agent API")

class RecommendRequest(BaseModel):
    summary: str

class RecommendResponse(BaseModel):
    recommendation: str

@app.post("/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest):
    if not GEMINI_KEY:
        raise HTTPException(status_code=503, detail="Gemini API key not configured")
    prompt = f"""You are a logistics solutions architect. Based on these dataset summaries:
{req.summary}

Suggest one high-impact problem to solve for the company. Explain why, list required components, and outline a short plan."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        text = response.text.strip() if hasattr(response, 'text') else str(response)
        return RecommendResponse(recommendation=text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
