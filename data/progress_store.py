# Simple in-memory progress store for dashboard
# In production, this should be in Supabase

from .progress_metadata import progress_metadata

_progress_data = {}
_resume_store = {}
_cache = {}

def get_cached(key):
    return _cache.get(key)

def set_cached(key, value):
    _cache[key] = value
    return True

def get_progress(user_id):
    user_progress = _progress_data.get(user_id, {
        "user_id": user_id,
        "completed_modules": [],
        "quiz_scores": {},
        "training_status": "Not Started",
        "interviews_completed": 0,
        "overall_score": 0,
        "quizzes_completed": 0,
        "resume_analyzed": False,
        "training_plans_viewed": 0
    })
    
    # Calculate derived values
    quiz_scores = list(user_progress.get("quiz_scores", {}).values())
    if quiz_scores:
        user_progress["averageScore"] = round(sum(quiz_scores) / len(quiz_scores), 1)
        user_progress["quizScores"] = quiz_scores  # For frontend compatibility
        user_progress["quizzesCompleted"] = len(quiz_scores)
        user_progress["completionPercent"] = min(100, len(quiz_scores) * 10)  # Simple progress calculation
    else:
        user_progress["averageScore"] = 0
        user_progress["quizScores"] = []
        user_progress["quizzesCompleted"] = 0
        user_progress["completionPercent"] = 0
    
    # Check if resume was analyzed
    if user_id in _resume_store:
        user_progress["resume_analyzed"] = True
    
    return user_progress

def record_event(user_id, event_type, details=None):
    if user_id not in _progress_data:
        _progress_data[user_id] = get_progress(user_id)
    
    print(f"📊 [Progress] Recording event: {event_type} for user {user_id}, details: {details}")
    
    # Simple logic to update progress based on event
    if event_type == "TRAINING_GENERATION":
        _progress_data[user_id]["training_status"] = "In Progress"
    elif event_type == "QUIZ_COMPLETED":
        score = details.get("score", 0) if details else 0
        role = details.get("role", "general") if details else "general"
        answers = details.get("answers", []) if details else []
        _progress_data[user_id]["quiz_scores"][role] = score
        # Add to quiz history for multiple attempts
        if "quiz_history" not in _progress_data[user_id]:
            _progress_data[user_id]["quiz_history"] = []
        _progress_data[user_id]["quiz_history"].append(score)
        
        # Add metadata
        progress_metadata.add_quiz_metadata(user_id, role, score, answers)
        print(f" [Progress] Stored quiz score: {score} for role {role}")
        print(f" [Progress] Quiz history: {_progress_data[user_id]['quiz_history']}")
    elif event_type == "INTERVIEW_COMPLETED":
        _progress_data[user_id]["interviews_completed"] = _progress_data[user_id].get("interviews_completed", 0) + 1
        score = details.get("score", 0) if details else 0
        current_score = _progress_data[user_id].get("overall_score", 0)
        _progress_data[user_id]["overall_score"] = (current_score + score) / 2 if current_score > 0 else score
    else:
        print(f" [Progress] Unknown event type: {event_type}")
    
    return _progress_data[user_id]

def save_resume(user_id, text, file_name):
    _resume_store[user_id] = {
        "text": text,
        "fileName": file_name,
        "timestamp": 0 # Placeholder
    }
    return True

def get_resume(user_id):
    return _resume_store.get(user_id)
