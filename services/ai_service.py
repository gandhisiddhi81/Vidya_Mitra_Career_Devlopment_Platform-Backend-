from services import gemini_service, grok_service
from typing import Optional, Dict, Any

async def analyze_resume(text: str, provider: str = "auto") -> Dict[str, Any]:
    if provider == "gemini" or (provider == "auto" and gemini_service.is_gemini_available()):
        try:
            return await gemini_service.analyze_resume(text)
        except Exception as e:
            if provider == "auto" and grok_service.is_grok_available():
                return await grok_service.analyze_resume(text)
            raise e
    elif provider == "grok" or (provider == "auto" and grok_service.is_grok_available()):
        return await grok_service.analyze_resume(text)
    raise Exception("No AI provider available")

async def generate_training_plan(role: str, provider: str = "auto") -> Dict[str, Any]:
    if provider == "gemini" or (provider == "auto" and gemini_service.is_gemini_available()):
        try:
            return await gemini_service.generate_training_plan(role)
        except Exception as e:
            if provider == "auto" and grok_service.is_grok_available():
                return await grok_service.generate_training_plan(role)
            raise e
    elif provider == "grok" or (provider == "auto" and grok_service.is_grok_available()):
        return await grok_service.generate_training_plan(role)
    raise Exception("No AI provider available")

async def generate_quiz(role: str, provider: str = "auto") -> Dict[str, Any]:
    if provider == "gemini" or (provider == "auto" and gemini_service.is_gemini_available()):
        try:
            return await gemini_service.generate_quiz(role)
        except Exception as e:
            if provider == "auto" and grok_service.is_grok_available():
                return await grok_service.generate_quiz(role)
            raise e
    elif provider == "grok" or (provider == "auto" and grok_service.is_grok_available()):
        return await grok_service.generate_quiz(role)
    raise Exception("No AI provider available")

async def generate_interview_questions(role: str, custom_role: Optional[str] = None, provider: str = "auto") -> Dict[str, Any]:
    if provider == "gemini" or (provider == "auto" and gemini_service.is_gemini_available()):
        try:
            return await gemini_service.generate_interview_questions(role, custom_role)
        except Exception as e:
            if provider == "auto" and grok_service.is_grok_available():
                return await grok_service.generate_interview_questions(role, custom_role)
            raise e
    elif provider == "grok" or (provider == "auto" and grok_service.is_grok_available()):
        return await grok_service.generate_interview_questions(role, custom_role)
    raise Exception("No AI provider available")
