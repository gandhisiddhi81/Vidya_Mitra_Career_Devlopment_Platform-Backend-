from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request, Body
from typing import Optional, Dict, Any
import io
from pypdf import PdfReader
import mammoth
from services import gemini_service, grok_service
import json
from pydantic import BaseModel
from data import progress_store

router = APIRouter()

class AnalyzeRequest(BaseModel):
    userId: Optional[str] = None
    text: Optional[str] = None
    fileName: Optional[str] = None

async def perform_analysis(text: str) -> Dict[str, Any]:
    print(f"⚡ [AI Analysis] Attempting with Grok first...")
    # Try Grok first, then Gemini
    if grok_service.is_grok_available():
        try:
            return await grok_service.analyze_resume(text)
        except Exception as e:
            print(f"❌ [AI Analysis] Grok failed: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("⚠️ [AI Analysis] Grok service is not available (key missing?)")
    
    print(f"⚡ [AI Analysis] Falling back to Gemini...")
    if gemini_service.is_gemini_available():
        try:
            return await gemini_service.analyze_resume(text)
        except Exception as e:
            print(f"❌ [AI Analysis] Gemini failed: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("⚠️ [AI Analysis] Gemini service is not available (key missing?)")
    
    raise HTTPException(
        status_code=503, 
        detail="No AI providers available or all failed to analyze resume. Check backend logs for details."
    )

@router.post("/analyze")
async def analyze_resume(
    request: Request,
    resume: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    userId: Optional[str] = Form(None),
    fileName: Optional[str] = Form(None)
):
    extracted_text = ""
    file_name = fileName
    user_id = userId

    print(f"📄 [Resume] New analysis request. User: {user_id}, File: {file_name}")

    # Check content type to decide how to parse
    content_type = request.headers.get("content-type", "")
    
    if "application/json" in content_type:
        try:
            body = await request.json()
            extracted_text = body.get("text", "")
            file_name = body.get("fileName", file_name)
            user_id = body.get("userId", user_id)
            print(f"🔍 [Resume] Extracted JSON text (len: {len(extracted_text)})")
        except Exception as e:
            print(f"❌ [Resume] JSON parse error: {e}")
    
    # If it's a multipart form (file upload)
    elif resume:
        file_name = resume.filename
        print(f"📂 [Resume] Processing uploaded file: {file_name} ({resume.content_type})")
        content = await resume.read()
        
        if resume.content_type == 'application/pdf':
            try:
                reader = PdfReader(io.BytesIO(content))
                extracted_text = ""
                num_pages = len(reader.pages)
                print(f"📄 [Resume] PDF has {num_pages} pages")
                
                for i, page in enumerate(reader.pages):
                    text_page = page.extract_text()
                    if text_page:
                        extracted_text += text_page + "\n"
                    else:
                        print(f"⚠️ [Resume] No text found on page {i+1}")
                
                if not extracted_text:
                    print(f"❌ [Resume] PDF extraction failed completely (empty text)")
                    raise HTTPException(status_code=400, detail="The PDF appears to be an image or scanned document. Please upload a text-based PDF or copy-paste the resume text.")
                
                print(f"📝 [Resume] Extracted PDF text (len: {len(extracted_text)})")
            except HTTPException:
                raise
            except Exception as e:
                print(f"❌ [Resume] PDF parse error: {e}")
                raise HTTPException(status_code=400, detail=f"Failed to parse PDF file: {str(e)}")
        elif resume.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            try:
                result = mammoth.extract_raw_text(io.BytesIO(content))
                extracted_text = result.value
                print(f"📝 [Resume] Extracted DOCX text (len: {len(extracted_text)})")
            except Exception as e:
                print(f"❌ [Resume] DOCX parse error: {e}")
                raise HTTPException(status_code=400, detail=f"Failed to parse DOCX: {e}")
        elif resume.content_type == 'text/plain':
            extracted_text = content.decode('utf-8')
            print(f"📝 [Resume] Extracted TXT text (len: {len(extracted_text)})")
        else:
            print(f"⚠️ [Resume] Unsupported file type: {resume.content_type}")
            raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # If it's a form-encoded text
    elif text:
        extracted_text = text
        print(f"📝 [Resume] Using form text (len: {len(extracted_text)})")

    if not extracted_text or len(extracted_text.strip()) < 50:
        print(f"⚠️ [Resume] Insufficient text extracted: {len(extracted_text) if extracted_text else 0} chars")
        raise HTTPException(status_code=400, detail="Could not extract sufficient text from resume. Please ensure the file is not empty or protected.")

    print(f"⚡ [Resume] Starting AI analysis with Grok/Gemini...")
    try:
        # Limit text length to avoid token limits and speed up
        max_chars = 6000
        analysis_text = extracted_text[:max_chars]
        if len(extracted_text) > max_chars:
            print(f"✂️ [Resume] Truncated text from {len(extracted_text)} to {max_chars} chars")
            
        result = await perform_analysis(analysis_text)
        print("✅ [Resume] Analysis completed successfully")
    except Exception as e:
        print(f"❌ [Resume] Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")
    
    return {
        "success": True,
        "data": result
    }

@router.post("/save/{user_id}")
async def save_resume(user_id: str, request: Request):
    try:
        body = await request.json()
        text = body.get("text", "")
        file_name = body.get("fileName", "")
        
        # Save to memory store for persistent session
        progress_store.save_resume(user_id, text, file_name)
        print(f"💾 Saving resume for user {user_id}: {file_name}")
        
        return {
            "success": True,
            "message": "Resume saved successfully"
        }
    except Exception as e:
        print(f"❌ Save resume failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def get_resume(user_id: str):
    # Fetch from memory store for persistent session
    resume_data = progress_store.get_resume(user_id)
    print(f"🔍 Fetching resume for user {user_id}")
    
    return {
        "success": True,
        "data": resume_data
    }
