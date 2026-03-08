import os
import google.generativeai as genai
from typing import Optional, List, Dict, Any
import json
import re

# Load environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("✅ Gemini AI initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Gemini AI: {e}")
else:
    print("⚠️ GEMINI_API_KEY not found in environment variables")

def is_gemini_available() -> bool:
    return bool(os.getenv("GEMINI_API_KEY"))

async def call_gemini(prompt: str, temperature: float = 0.3) -> Dict[str, Any]:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise Exception("Gemini AI is not available (key missing).")

    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel(
            model_name="models/gemini-pro-latest",
            generation_config={
                "temperature": temperature,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )

        response = await model.generate_content_async(prompt)
        text = response.text
        
        # Remove thoughts or reasoning tags if present
        cleaned_text = re.sub(r'<think>[\s\S]*?</think>', '', text)
        cleaned_text = cleaned_text.strip()
        
        # Remove markdown formatting if present
        if "```json" in cleaned_text:
            cleaned_text = cleaned_text.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned_text:
            cleaned_text = cleaned_text.split("```")[1].split("```")[0].strip()

        json_match = re.search(r'\{[\s\S]*\}', cleaned_text)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except Exception as e:
                print(f"❌ [Gemini] JSON parse error: {e}")
                raise Exception("Invalid JSON format from Gemini")
        
        raise Exception("No JSON found in Gemini response")
    except Exception as e:
        print(f"Gemini API Error: {e}")
        raise e

async def generate_text(prompt: str, temperature: float = 0.5) -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise Exception("Gemini AI is not available (key missing).")

    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Text API Error: {e}")
        raise e

async def analyze_resume(resume_text: str) -> Dict[str, Any]:
    prompt = f"""
    Analyze this resume and provide a detailed assessment.
    Resume text: {resume_text}

    Return ONLY a JSON object with this exact structure:
    {{
      "score": number (0-100),
      "strengths": ["string", ...],
      "weaknesses": ["string", ...],
      "suggestions": ["string", ...],
      "recommendedRoles": [
        {{
          "role": "string",
          "matchPercentage": number,
          "requiredSkills": ["string", ...],
          "skillGaps": ["string", ...]
        }}
      ]
    }}
    """
    return await call_gemini(prompt)

async def generate_training_plan(role: str) -> Dict[str, Any]:
    prompt = f"""
    Create a highly detailed professional training plan for the role of "{role}".
    The plan must include modules, hands-on projects, and real-world skills.
    
    Return ONLY a JSON object with this exact structure:
    {{
      "role": "{role}",
      "description": "string",
      "skillsRequired": ["string", ...],
      "modules": [
        {{
          "title": "string",
          "description": "string",
          "topics": ["string", ...],
          "duration": "string"
        }}
      ],
      "projects": [
        {{
          "title": "string",
          "description": "string",
          "difficulty": "Beginner|Intermediate|Advanced",
          "technologies": ["string", ...]
        }}
      ],
      "certifications": ["string", ...]
    }}
    """
    return await call_gemini(prompt, 0.5)

async def evaluate_interview(role: str, questions: List[str], answers: List[str]) -> Dict[str, Any]:
    # Combine questions and answers for the prompt
    qa_pairs = []
    for q, a in zip(questions, answers):
        qa_pairs.append(f"Q: {q}\nA: {a}")
    
    qa_text = "\n\n".join(qa_pairs)
    
    prompt = f"""
    Evaluate the following interview answers for the role of "{role}".
    Provide a comprehensive score, feedback for each question, overall strengths, and areas for improvement.
    
    Interview Data:
    {qa_text}
    
    Return ONLY a JSON object with this structure:
    {{
      "score": number (0-100),
      "finalAdvice": "overall summary feedback string",
      "feedback": [
        {{
          "questionIndex": number (starting from 0),
          "rating": number (1-10),
          "feedback": "string explaining why this rating was given",
          "improvedAnswer": "string"
        }}
      ],
      "strengths": ["string", "string", ...],
      "areasForImprovement": ["string", "string", ...]
    }}
    """
    return await call_gemini(prompt, 0.4)

async def generate_quiz(role_or_skill: str) -> Dict[str, Any]:
    prompt = f"""
    Generate a quiz with 5 multiple-choice questions for "{role_or_skill}".
    
    Return ONLY a JSON object with this exact structure:
    {{
      "title": "Quiz for {role_or_skill}",
      "questions": [
        {{
          "question": "string",
          "options": ["string", "string", "string", "string"],
          "correctAnswer": 0, (index of the correct option)
          "explanation": "string"
        }}
      ]
    }}
    """
    return await call_gemini(prompt, 0.4)

async def generate_interview_questions(role: str, custom_role: Optional[str] = None) -> Dict[str, Any]:
    target_role = custom_role or role
    prompt = f"""
    Generate EXACTLY 10 interview questions for the role: "{target_role}".
    The questions should be distributed as:
    - 4 Technical questions
    - 3 Behavioral questions
    - 3 Coding/Problem-solving questions
    
    Return ONLY a JSON object with this exact structure:
    {{
      "role": "{target_role}",
      "technical": ["question 1", "question 2", "question 3", "question 4"],
      "behavioral": ["question 5", "question 6", "question 7"],
      "coding": ["question 8", "question 9", "question 10"]
    }}
    """
    return await call_gemini(prompt, 0.5)
