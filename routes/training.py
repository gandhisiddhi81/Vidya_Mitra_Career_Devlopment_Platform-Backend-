from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from services import gemini_service, grok_service, youtube_service, certification_service
import asyncio
from data import progress_store

router = APIRouter()

class TrainingRequest(BaseModel):
    role: str
    userSkills: Optional[List[str]] = None
    userId: Optional[str] = None

@router.post("/generate")
async def generate_training(request: TrainingRequest):
    if not request.role:
        raise HTTPException(status_code=400, detail="Role is required")

    # Check cache first
    cache_key = f"training_{request.role.lower()}"
    cached_data = progress_store.get_cached(cache_key)
    if cached_data:
        print(f"🚀 Returning cached training plan for {request.role}")
        if request.userId:
            progress_store.record_event(request.userId, "TRAINING_GENERATION", {"role": request.role})
        return {"success": True, "data": cached_data}

    # Start all tasks in parallel to speed up response
    async def get_ai_plan():
        # Try Grok first, then Gemini
        if grok_service.is_grok_available():
            try:
                return await grok_service.generate_training_plan(request.role)
            except Exception as e:
                print(f"Grok training plan generation failed, trying Gemini: {e}")
                if gemini_service.is_gemini_available():
                    return await gemini_service.generate_training_plan(request.role)
                else:
                    raise e
        elif gemini_service.is_gemini_available():
            return await gemini_service.generate_training_plan(request.role)
        else:
            raise HTTPException(status_code=503, detail="AI services are not available")

    # Launch all external calls concurrently
    ai_task = asyncio.create_task(get_ai_plan())
    youtube_videos_task = asyncio.create_task(youtube_service.search_videos(f"{request.role} tutorials for beginners", 5))
    youtube_playlists_task = asyncio.create_task(youtube_service.search_playlists(f"{request.role} full course", 3))
    real_certs_task = asyncio.create_task(certification_service.get_recommended_certifications(request.role))
    
    # Wait for all of them to finish
    result, youtube_videos, youtube_playlists, real_certs = await asyncio.gather(
        ai_task, youtube_videos_task, youtube_playlists_task, real_certs_task
    )

    training_plan = {
        "role": result.get("role", request.role),
        "description": result.get("description", ""),
        "skillsRequired": result.get("skillsRequired", []),
        "modules": result.get("modules", []),
        "projects": result.get("projects", []),
        "certifications": real_certs if real_certs else result.get("certifications", []),
        "youtubeResources": {
            "videos": youtube_videos,
            "playlists": youtube_playlists
        }
    }

    if request.userId:
        progress_store.record_event(request.userId, "TRAINING_GENERATION", {"role": request.role})

    # Save to cache for future requests
    progress_store.set_cached(cache_key, training_plan)

    return {
        "success": True,
        "data": training_plan
    }

@router.get("/plan/{role}")
async def get_training_plan(role: str, userId: Optional[str] = None):
    # This should fetch from a store
    # For now, let's generate a new plan if it doesn't exist
    print(f"📚 Fetching training plan for user {userId} (role: {role})")
    try:
        # Check if we can generate a plan
        request = TrainingRequest(role=role, userId=userId)
        return await generate_training(request)
    except Exception as e:
        print(f"❌ Failed to fetch training plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{role}")
async def get_training_plan_legacy(role: str, userId: Optional[str] = None):
    return await get_training_plan(role, userId)
