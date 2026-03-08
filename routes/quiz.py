from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from services import gemini_service, grok_service
from data import progress_store

router = APIRouter()

class QuizRequest(BaseModel):
    role: str
    userId: Optional[str] = None

@router.post("/generate")
async def generate_quiz(request: QuizRequest):
    if not request.role:
        raise HTTPException(status_code=400, detail="Role is required")

    # Generate fresh questions each time (no caching for dynamic content)
    print(f"🎯 Generating fresh quiz for {request.role}")
    
    result = None

    # Try Grok first, then Gemini
    if grok_service.is_grok_available():
        try:
            result = await grok_service.generate_quiz(request.role)
            print(f"✅ Generated quiz using Grok for {request.role}")
        except Exception as e:
            print(f"Grok quiz generation failed, trying Gemini: {e}")
            if gemini_service.is_gemini_available():
                result = await gemini_service.generate_quiz(request.role)
                print(f"✅ Generated quiz using Gemini for {request.role}")
            else:
                raise e
    elif gemini_service.is_gemini_available():
        result = await gemini_service.generate_quiz(request.role)
        print(f"✅ Generated quiz using Gemini for {request.role}")
    else:
        raise HTTPException(status_code=503, detail="AI services are not available")

    # Ensure result has questions
    questions = result.get("questions", [])
    if not questions:
        raise HTTPException(status_code=500, detail="Failed to generate quiz questions")

    if request.userId:
        progress_store.record_event(request.userId, "QUIZ_STARTED", {"role": request.role})

    quiz_data = {
        "role": request.role,
        "questions": questions
    }

    return {
        "success": True,
        "data": quiz_data
    }

@router.get("/{role}")
async def get_quiz_by_role(role: str):
    # Generate fresh quiz for role using same logic as POST (no caching)
    print(f"🎯 Generating fresh quiz for {role} via GET")
    
    result = None

    # Try Grok first, then Gemini
    if grok_service.is_grok_available():
        try:
            result = await grok_service.generate_quiz(role)
            print(f"✅ Generated quiz using Grok for {role}")
        except Exception as e:
            print(f"Grok quiz generation failed, trying Gemini: {e}")
            if gemini_service.is_gemini_available():
                result = await gemini_service.generate_quiz(role)
                print(f"✅ Generated quiz using Gemini for {role}")
            else:
                raise e
    elif gemini_service.is_gemini_available():
        result = await gemini_service.generate_quiz(role)
        print(f"✅ Generated quiz using Gemini for {role}")
    else:
        raise HTTPException(status_code=503, detail="AI services are not available")

    # Ensure result has questions
    questions = result.get("questions", [])
    if not questions:
        raise HTTPException(status_code=500, detail="Failed to generate quiz questions")

    quiz_data = {
        "role": role,
        "questions": questions
    }

    return {
        "success": True,
        "data": quiz_data
    }

class QuizSubmission(BaseModel):
    userId: str
    role: str
    answers: List[Any]
    score: Optional[float] = None

@router.post("/submit")
async def submit_quiz(submission: QuizSubmission):
    print(f"📝 Quiz submitted for user {submission.userId} (role: {submission.role}, score: {submission.score})")
    
    # Update progress in memory
    progress_store.record_event(submission.userId, "QUIZ_COMPLETED", {
        "role": submission.role,
        "score": submission.score or 0
    })
    
    # Sync to Supabase if available
    try:
        from data import progress_store
        memory_data = progress_store.get_progress(submission.userId)
        
        if supabase:
            # Update existing record in Supabase
            update_data = {
                "user_id": submission.userId,
                "completed_modules": json.dumps(memory_data.get("completed_modules", [])),
                "quiz_scores": json.dumps(memory_data.get("quiz_scores", {})),
                "quiz_history": json.dumps(memory_data.get("quiz_history", [])),
                "training_status": memory_data.get("training_status", "Not Started"),
                "interviews_completed": memory_data.get("interviews_completed", 0),
                "overall_score": memory_data.get("overall_score", 0),
                "resume_analyzed": memory_data.get("resume_analyzed", False),
                "training_plans_viewed": memory_data.get("training_plans_viewed", 0)
            }
            
            result = supabase.table("user_progress").update(update_data).eq("user_id", submission.userId).execute()
            print(f"✅ [Supabase] Synced quiz progress for {submission.userId}")
            
    except Exception as e:
        print(f"❌ [Supabase] Failed to sync quiz progress: {e}")
    
    return {
        "success": True,
        "data": {
            "userId": submission.userId,
            "role": submission.role,
            "score": submission.score or 0
        }
    }

@router.post("/evaluate")
async def evaluate_quiz(submission: QuizSubmission):
    # This could call AI to evaluate, but usually MCQs are graded on frontend
    # For now, just return success
    return {
        "success": True,
        "data": {
            "score": submission.score or 0,
            "feedback": "Great job on completing the quiz!"
        }
    }
