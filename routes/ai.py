from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from services import gemini_service, grok_service, certification_service
import os
import requests

router = APIRouter()

class AIRequest(BaseModel):
    text: Optional[str] = None
    role: Optional[str] = None
    userId: Optional[str] = None
    provider: Optional[str] = "auto"

@router.get("/providers")
async def get_providers():
    return {
        "gemini": gemini_service.is_gemini_available(),
        "grok": grok_service.is_grok_available()
    }

@router.post("/analyze-resume")
async def analyze_resume(request: AIRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is required")

    # For simplicity, we use grok if available, then gemini
    if request.provider == "grok" or (request.provider == "auto" and grok_service.is_grok_available()):
        try:
            return await grok_service.analyze_resume(request.text)
        except Exception as e:
            if request.provider == "auto" and gemini_service.is_gemini_available():
                return await gemini_service.analyze_resume(request.text)
            raise e
    elif request.provider == "gemini" or (request.provider == "auto" and gemini_service.is_gemini_available()):
        return await gemini_service.analyze_resume(request.text)
    
    raise HTTPException(status_code=503, detail="Requested AI provider not available")

@router.get("/career-news/{role}")
async def get_career_news(role: str):
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    if not NEWS_API_KEY:
        return {"success": False, "error": "News API not configured"}

    try:
        response = requests.get('https://newsapi.org/v2/everything', params={
            'q': f'{role} career industry trends',
            'sortBy': 'relevancy',
            'pageSize': 5,
            'apiKey': NEWS_API_KEY,
            'language': 'en'
        })
        response.raise_for_status()
        return {"success": True, "data": response.json().get('articles', [])}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/career-advice")
async def get_career_advice(request: AIRequest):
    if not request.role:
        raise HTTPException(status_code=400, detail="Role is required")

    prompt = f"Provide expert career advice for a {request.role} focusing on current industry trends and high-demand skills."
    
    # Try Grok first
    if grok_service.is_grok_available():
        try:
            messages = [
                {"role": "system", "content": "You are a career expert advice provider."},
                {"role": "user", "content": prompt}
            ]
            response = await grok_service.make_request(messages)
            return {"success": True, "data": response}
        except Exception as e:
            print(f"Grok failed for career advice, trying Gemini: {e}")
            # Fallback to Gemini handled below
    
    # Try Gemini next
    if gemini_service.is_gemini_available():
        try:
            response = await gemini_service.generate_text(prompt)
            return {"success": True, "data": response}
        except Exception as e:
            print(f"Gemini failed for career advice: {e}")
    
    return {"success": False, "error": "AI service not available"}
