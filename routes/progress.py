from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import os
from supabase import create_client, Client
from data import progress_store

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Supabase client: {e}")

class ProgressUpdate(BaseModel):
    userId: str
    completed_modules: Optional[List[str]] = None
    quiz_scores: Optional[Dict[str, float]] = None
    training_status: Optional[str] = None

@router.get("/metadata/{user_id}")
async def get_progress_metadata(user_id: str):
    """Get detailed progress metadata for a user"""
    try:
        from data.progress_metadata import progress_metadata
        metadata = progress_metadata.get_progress_summary(user_id)
        return {"success": True, "data": metadata}
    except Exception as e:
        print(f"❌ [Metadata] Error: {e}")
        return {"success": False, "error": str(e)}

@router.get("/{user_id}")
async def get_user_progress(user_id: str):
    # Get data from memory store (which has the latest data)
    memory_data = progress_store.get_progress(user_id)
    
    # Try to sync with Supabase
    if supabase:
        try:
            # Check if user exists in Supabase
            existing = supabase.table("user_progress").select("*").eq("user_id", user_id).execute()
            
            if existing.data:
                # Update existing record
                update_data = {
                    "user_id": user_id,
                    "completed_modules": memory_data.get("completed_modules", []),
                    "quiz_scores": memory_data.get("quiz_scores", {}),
                    "quiz_history": memory_data.get("quiz_history", []),
                    "training_status": memory_data.get("training_status", "Not Started"),
                    "interviews_completed": memory_data.get("interviews_completed", 0),
                    "overall_score": memory_data.get("overall_score", 0),
                    "resume_analyzed": memory_data.get("resume_analyzed", False),
                    "training_plans_viewed": memory_data.get("training_plans_viewed", 0)
                }
                
                result = supabase.table("user_progress").update(update_data).eq("user_id", user_id).execute()
                print(f"✅ [Supabase] Updated progress for {user_id}")
            else:
                # Insert new record
                insert_data = {
                    "user_id": user_id,
                    "completed_modules": memory_data.get("completed_modules", []),
                    "quiz_scores": memory_data.get("quiz_scores", {}),
                    "quiz_history": memory_data.get("quiz_history", []),
                    "training_status": memory_data.get("training_status", "Not Started"),
                    "interviews_completed": memory_data.get("interviews_completed", 0),
                    "overall_score": memory_data.get("overall_score", 0),
                    "resume_analyzed": memory_data.get("resume_analyzed", False),
                    "training_plans_viewed": memory_data.get("training_plans_viewed", 0)
                }
                
                result = supabase.table("user_progress").insert(insert_data).execute()
                print(f"✅ [Supabase] Inserted progress for {user_id}")
                
        except Exception as e:
            print(f"❌ [Supabase] Error: {e}")
    
    # Always return memory data (most up-to-date)
    return {"success": True, "data": memory_data}

@router.put("/")
async def update_progress(update: ProgressUpdate):
    # Update memory always
    progress_store.record_event(update.userId, "UPDATE", {
        "completed_modules": update.completed_modules,
        "quiz_scores": update.quiz_scores,
        "training_status": update.training_status
    })

    # Try Supabase if configured
    if supabase:
        try:
            # Upsert user progress
            data = {
                "user_id": update.userId,
                "completed_modules": update.completed_modules,
                "quiz_scores": update.quiz_scores,
                "training_status": update.training_status
            }
            # Filter out None values
            data = {k: v for k, v in data.items() if v is not None}
            response = supabase.table("user_progress").upsert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            print(f"Supabase PUT Error (persisted in memory only): {e}")

    return {"success": True, "data": progress_store.get_progress(update.userId)}

class RolesViewedRequest(BaseModel):
    userId: str

@router.post("/roles-viewed")
async def mark_roles_viewed(request: RolesViewedRequest):
    # In production, save to Supabase
    print(f"💼 Marking roles as viewed for user {request.userId}")
    return {"success": True}
