from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from services import gemini_service, grok_service

router = APIRouter()

class RolesRequest(BaseModel):
    resumeText: str

ROLES_LIST = [
  { "id": "software-engineer", "label": "Software Engineer", "description": "Programming, algorithms, and system design" },
  { "id": "frontend-developer", "label": "Frontend Developer", "description": "UI/UX, React, CSS, and web technologies" },
  { "id": "backend-developer", "label": "Backend Developer", "description": "Server-side, databases, and APIs" },
  { "id": "full-stack-developer", "label": "Full-stack Developer", "description": "End-to-end web development" },
  { "id": "data-scientist", "label": "Data Scientist", "description": "Python, ML, statistics, and data analysis" },
  { "id": "data-analyst", "label": "Data Analyst", "description": "SQL, Excel, visualization, and analytics" },
  { "id": "product-manager", "label": "Product Manager", "description": "Strategy, roadmap, and product development" },
  { "id": "devops-engineer", "label": "DevOps Engineer", "description": "CI/CD, cloud infrastructure, and automation" },
]

@router.get("/")
async def get_roles():
    return {"success": True, "data": ROLES_LIST}

@router.post("/matching")
async def get_matching_roles(request: RolesRequest):
    if not request.resumeText:
        raise HTTPException(status_code=400, detail="Resume text is required")

    prompt = f"""
    Based on the following resume text, suggest the top 5 best matching career roles.
    For each role, provide:
    1. Role title
    2. Match percentage
    3. Key skills matched
    4. Skill gaps (what's missing)
    5. A brief learning roadmap to bridge the gaps
    
    Resume text: {request.resumeText}
    
    Return ONLY a JSON array of objects with this structure:
    [
      {{
        "role": "string",
        "matchPercentage": number,
        "matchedSkills": ["string", ...],
        "skillGaps": ["string", ...],
        "roadmap": ["string", ...]
      }}
    ]
    """
    
    result = None
    if gemini_service.is_gemini_available():
        try:
            result = await gemini_service.call_gemini(prompt)
        except Exception as e:
            print(f"Gemini failed for roles matching: {e}")
    
    if not result and grok_service.is_grok_available():
        try:
            response = await grok_service.make_request([
                {"role": "system", "content": "You are a career matching expert. Return ONLY JSON."},
                {"role": "user", "content": prompt}
            ])
            result = grok_service.parse_json_response(response)
        except Exception as e:
            print(f"Grok failed for roles matching: {e}")
            
    if not result:
        raise HTTPException(status_code=500, detail="Failed to get role matching results")
        
    return {
        "success": True,
        "data": result
    }
