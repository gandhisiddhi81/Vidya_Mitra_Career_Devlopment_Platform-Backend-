import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="VidyaMitra 2.0 AI Career Assistant")

# Configure CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
origins = [
    FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://vidya-mitra-career-devlopment-platform-r457.onrender.com",
    "https://vidya-mitra-frontend.onrender.com",
    "https://vidya-mitra-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key Validation
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

print("\n" + "="*50)
print("🔐 VidyaMitra 2.0 - Python Backend")
print("="*50)
print(f"✅ Gemini API: {'Configured' if GEMINI_API_KEY else 'Missing'}")
print(f"✅ Grok API: {'Configured' if GROK_API_KEY else 'Missing'}")
print(f"✅ YouTube API: {'Configured' if YOUTUBE_API_KEY else 'Missing'}")
print(f"✅ News API: {'Configured' if NEWS_API_KEY else 'Missing'}")
print("="*50 + "\n")

@app.get("/")
async def root():
    return {"message": "VidyaMitra 2.0 Python API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "VidyaMitra 2.0 Backend"}

# Include routes
from routes import resume, training, quiz, interview, progress, ai, roles
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(training.router, prefix="/api/training", tags=["Training"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(interview.router, prefix="/api/interview", tags=["Interview"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(roles.router, prefix="/api/roles", tags=["Roles"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
