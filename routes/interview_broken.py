from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from services import gemini_service, grok_service
import uuid
import datetime
from data import progress_store
import json

router = APIRouter()

# Simple in-memory storage for sessions (in production, use Supabase)
interview_sessions = {}

class InterviewStartRequest(BaseModel):
    role: str
    userId: Optional[str] = None
    customRole: Optional[str] = None

@router.post("/start")
async def start_interview(request: InterviewStartRequest):
    if not request.role and not request.customRole:
        raise HTTPException(status_code=400, detail="Role is required")

    role_key = request.customRole or request.role
        session = {
            "sessionId": session_id,
            "role": role_key,
            "questions": cached_questions,
            "startedAt": datetime.datetime.now().isoformat(),
            "answers": []
        }
        interview_sessions[session_id] = session
        
        return {
            "success": True,
            "data": {
                "sessionId": session_id,
                "role": session["role"],
                "questions": [{
                    "index": i,
                    "question": q["question"],
                    "category": q["category"]
                } for i, q in enumerate(cached_questions)]
            }
        }

    result = None
    
    # Try Gemini first, then Grok as fallback
    if gemini_service.is_gemini_available():
        try:
            print("🔮 Trying Gemini first for interview questions")
            result = await gemini_service.generate_interview_questions(request.role, request.customRole)
            print(f"✅ Gemini generated {len(result.get('technical', [])) + len(result.get('behavioral', [])) + len(result.get('coding', []))} questions")
        except Exception as e:
            print(f"Gemini interview questions failed, trying Grok: {e}")
            if grok_service.is_grok_available():
                result = await grok_service.generate_interview_questions(request.role, request.customRole)
                print(f"✅ Grok generated {len(result.get('technical', [])) + len(result.get('behavioral', [])) + len(result.get('coding', []))} questions")
            else:
                raise e
    elif grok_service.is_grok_available():
        try:
            print("🔮 Using Grok for interview questions (Gemini unavailable)")
            result = await grok_service.generate_interview_questions(request.role, request.customRole)
            print(f"✅ Grok generated {len(result.get('technical', [])) + len(result.get('behavioral', [])) + len(result.get('coding', []))} questions")
        except Exception as e:
            print(f"Grok interview questions failed: {e}")
            raise e
    else:
        raise HTTPException(status_code=503, detail="AI services are not available")

    # Normalize questions
    technical = [{"question": q, "category": "technical"} for q in result.get("technical", [])]
    behavioral = [{"question": q, "category": "behavioral"} for q in result.get("behavioral", [])]
    coding = [{"question": q, "category": "coding"} for q in result.get("coding", [])]
    
    all_questions = technical + behavioral + coding

    if not all_questions:
        raise HTTPException(status_code=500, detail="Failed to generate interview questions")

    if request.userId:
        progress_store.record_event(request.userId, "INTERVIEW_STARTED", {"role": request.customRole or request.role})

    # Save to cache
    progress_store.set_cached(cache_key, all_questions)

    session_id = str(uuid.uuid4())
    session = {
        "sessionId": session_id,
        "role": request.customRole or request.role,
        "questions": all_questions,
        "startedAt": datetime.datetime.now().isoformat(),
        "answers": []
    }

    interview_sessions[session_id] = session

    return {
        "success": True,
        "data": {
            "sessionId": session_id,
            "role": session["role"],
            "questions": [{
                "index": i,
                "question": q["question"],
                "category": q["category"]
            } for i, q in enumerate(all_questions)]
        }
    }

class InterviewFeedbackRequest(BaseModel):
    userId: Optional[str] = None
    role: str
    answers: List[Dict[str, Any]]

@router.post("/feedback")
async def get_interview_feedback(request: InterviewFeedbackRequest):
    if not request.answers:
        raise HTTPException(status_code=400, detail="Answers are required")

    # Use AI to evaluate answers
    questions = [a.get("question", "") for a in request.answers]
    answers = [a.get("text", "") for a in request.answers]

    # Final data to return
    final_result = None

    # Try Grok/Groq first
    if grok_service.is_grok_available():
        try:
            final_result = await grok_service.evaluate_interview(request.role, questions, answers)
        except Exception as e:
            print(f"Grok failed for interview feedback: {e}")
    
    if not final_result and gemini_service.is_gemini_available():
        try:
            final_result = await gemini_service.evaluate_interview(request.role, questions, answers)
        except Exception as e:
            print(f"Gemini failed for interview feedback: {e}")
    
    # Simple fallback if both AI services fail
    if not final_result:
        final_result = {
            "overallScore": 75,
            "overallFeedback": "Good job! You answered the questions well. Keep practicing to improve your confidence.",
            "detailedAnalysis": [
                {
                    "question": q,
                    "score": 75,
                    "feedback": "Your answer was reasonable.",
                    "improvedAnswer": "Consider adding more specific examples."
                } for q in questions
            ]
        }

    if request.userId:
        progress_store.record_event(request.userId, "INTERVIEW_COMPLETED", {
            "role": request.role,
            "score": final_result.get("overallScore", final_result.get("score", 75))
        })

    return {
        "success": True,
        "data": final_result
    }

class InterviewEvaluateRequest(BaseModel):
    sessionId: Optional[str] = None
    role: str
    questions: List[str]
    answers: List[str]
    userId: Optional[str] = None

@router.post("/evaluate")
async def evaluate_interview(request: InterviewEvaluateRequest):
    result = None
    if gemini_service.is_gemini_available():
        try:
            result = await gemini_service.evaluate_interview(request.role, request.questions, request.answers)
        except Exception as e:
            print(f"Gemini failed for interview evaluation: {e}")
            if grok_service.is_grok_available():
                result = await grok_service.evaluate_interview(request.role, request.questions, request.answers)
            else:
                raise e
    elif grok_service.is_grok_available():
        result = await grok_service.evaluate_interview(request.role, request.questions, request.answers)
    else:
        # Simple fallback
        result = {
            "score": 75,
            "feedback": "Good job! You answered the questions well. Keep practicing to improve your confidence.",
            "strengths": ["Clear communication", "Technical knowledge"],
            "improvements": ["More detailed answers", "Structure your responses better"]
        }

    if request.userId:
        progress_store.record_event(request.userId, "INTERVIEW_COMPLETED", {
            "role": request.role,
            "score": result.get("score", 0)
        })

    return {
        "success": True,
        "data": result
    }

@router.get("/questions/{role}")
async def get_interview_questions(role: str):
    # This can reuse the start_interview logic or fetch from a store
    # For now, let's just generate new questions
    try:
        # Try Grok first since Gemini has quota issues
        if grok_service.is_grok_available():
            result = await grok_service.generate_interview_questions(role)
            print(f"✅ Generated interview questions using Grok for {role}")
        elif gemini_service.is_gemini_available():
            result = await gemini_service.generate_interview_questions(role)
            print(f"✅ Generated interview questions using Gemini for {role}")
        else:
            # Fallback to simple questions
            result = {"technical": ["Tell me about yourself"], "behavioral": ["Why do you want this job?"], "coding": []}
            
        technical = [{"question": q, "category": "technical"} for q in result.get("technical", [])]
        behavioral = [{"question": q, "category": "behavioral"} for q in result.get("behavioral", [])]
        coding = [{"question": q, "category": "coding"} for q in result.get("coding", [])]
        
        all_questions = technical + behavioral + coding
        
        return {
            "success": True,
            "data": {
                "role": role,
                "questions": all_questions
            }
        }
    except Exception as e:
        print(f"❌ Failed to get interview questions: {e}")
        # Fallback to simple questions
        fallback_questions = [
            {"question": "Tell me about yourself and your experience.", "category": "behavioral"},
            {"question": "Why are you interested in this role?", "category": "behavioral"},
            {"question": "What technical skills do you have for this position?", "category": "technical"},
            {"question": "Describe a challenging project you worked on.", "category": "technical"},
            {"question": "Where do you see yourself in 5 years?", "category": "behavioral"}
        ]
        
        return {
            "success": True,
            "data": {
                "role": role,
                "questions": fallback_questions
            }
        }
