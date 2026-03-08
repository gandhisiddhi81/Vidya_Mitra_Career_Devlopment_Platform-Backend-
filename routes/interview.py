# Interview Routes - RESTORED WORKING VERSION

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import datetime
import uuid

from services import gemini_service, grok_service
from data import progress_store

router = APIRouter(tags=["interview"])

# Interview session storage (in production, use database)
interview_sessions = {}

class InterviewStartRequest(BaseModel):
    role: str
    userId: Optional[str] = None
    customRole: Optional[str] = None

class InterviewQuestionRequest(BaseModel):
    role: str
    customRole: Optional[str] = None

class InterviewSubmitRequest(BaseModel):
    sessionId: str
    userId: Optional[str] = None
    role: str
    answers: List[dict]

class InterviewFeedbackRequest(BaseModel):
    userId: str
    role: str
    answers: List[dict]

@router.post("/start")
async def start_interview(request: InterviewStartRequest):
    if not request.role and not request.customRole:
        raise HTTPException(status_code=400, detail="Role is required")

    role_key = request.customRole or request.role
    
    # Generate questions
    question_request = InterviewQuestionRequest(role=request.role, customRole=request.customRole)
    questions_response = await get_interview_questions(question_request.role)
    
    if not questions_response.get("success"):
        raise HTTPException(status_code=500, detail="Failed to generate interview questions")
    
    all_questions = questions_response["data"]["questions"]
    
    session_id = str(uuid.uuid4())
    session = {
        "sessionId": session_id,
        "role": role_key,
        "questions": all_questions,
        "startedAt": datetime.datetime.now().isoformat(),
        "answers": []
    }
    
    interview_sessions[session_id] = session
    
    if request.userId:
        progress_store.record_event(request.userId, "INTERVIEW_STARTED", {"role": role_key})
    
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

@router.get("/questions/{role}")
async def get_interview_questions(role: str):
    print(f"🎭 Generating interview questions for role: {role}")
    
    request = InterviewQuestionRequest(role=role)
    
    # Try Grok first, then Gemini
    result = None
    
    if grok_service.is_grok_available():
        try:
            result = await grok_service.generate_interview_questions(request.role, request.customRole)
            print(f"✅ Grok generated interview questions: {len(result.get('technical', [])) + len(result.get('behavioral', [])) + len(result.get('coding', []))} total")
        except Exception as e:
            print(f"Grok interview questions failed, trying Gemini: {e}")
            if gemini_service.is_gemini_available():
                result = await gemini_service.generate_interview_questions(request.role, request.customRole)
                print(f"✅ Gemini generated interview questions: {len(result.get('technical', [])) + len(result.get('behavioral', [])) + len(result.get('coding', []))} total")
            else:
                raise e
    elif gemini_service.is_gemini_available():
        result = await gemini_service.generate_interview_questions(request.role, request.customRole)
        print(f"✅ Gemini generated interview questions: {len(result.get('technical', [])) + len(result.get('behavioral', [])) + len(result.get('coding', []))} total")
    else:
        raise HTTPException(status_code=503, detail="AI services are not available")
    
    # Normalize questions
    technical = [{"question": q, "category": "technical"} for q in result.get("technical", [])]
    behavioral = [{"question": q, "category": "behavioral"} for q in result.get("behavioral", [])]
    coding = [{"question": q, "category": "coding"} for q in result.get("coding", [])]
    
    all_questions = technical + behavioral + coding
    
    if not all_questions:
        raise HTTPException(status_code=500, detail="Failed to generate interview questions")
    
    return {
        "success": True,
        "data": {
            "role": role,
            "questions": all_questions
        }
    }

@router.post("/feedback")
async def evaluate_interview(request: InterviewFeedbackRequest):
    print(f"🎭 Evaluating interview for user {request.userId}")
    
    # Try Grok first, then Gemini
    result = None
    
    if grok_service.is_grok_available():
        try:
            result = await grok_service.evaluate_interview(request.role, request.answers)
            print(f"✅ Grok evaluated interview: {result.get('overallScore', 0)}% score")
        except Exception as e:
            print(f"Grok interview evaluation failed, trying Gemini: {e}")
            if gemini_service.is_gemini_available():
                result = await gemini_service.evaluate_interview(request.role, request.answers)
                print(f"✅ Gemini evaluated interview: {result.get('overallScore', 0)}% score")
            else:
                raise e
    elif gemini_service.is_gemini_available():
        result = await gemini_service.evaluate_interview(request.role, request.answers)
        print(f"✅ Gemini evaluated interview: {result.get('overallScore', 0)}% score")
    else:
        raise HTTPException(status_code=503, detail="AI services are not available")
    
    # Record interview completion
    progress_store.record_event(request.userId, "INTERVIEW_COMPLETED", {
        "role": request.role,
        "score": result.get("overallScore", 0)
    })
    
    return {
        "success": True,
        "data": result
    }

@router.post("/submit")
async def submit_interview(request: InterviewSubmitRequest):
    session_id = request.sessionId
    
    if session_id not in interview_sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    session = interview_sessions[session_id]
    
    # Update session with answers
    session["answers"] = request.answers
    session["completedAt"] = datetime.datetime.now().isoformat()
    
    # Evaluate interview
    feedback_request = InterviewFeedbackRequest(
        userId=request.userId,
        role=request.role,
        answers=request.answers
    )
    
    feedback_response = await evaluate_interview(feedback_request)
    
    return {
        "success": True,
        "data": {
            "sessionId": session_id,
            "feedback": feedback_response["data"]
        }
    }

@router.get("/session/{session_id}")
async def get_interview_session(session_id: str):
    if session_id not in interview_sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    return {
        "success": True,
        "data": interview_sessions[session_id]
    }
