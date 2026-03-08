import os
import httpx
from typing import Optional, List, Dict, Any
import json
import re
import asyncio

# Load environment variables
GROK_API_KEY = os.getenv("GROK_API_KEY")

def is_grok_available() -> bool:
    key = os.getenv("GROK_API_KEY")
    if not key:
        print("⚠️ [AI] GROK_API_KEY is not set in environment")
    return bool(key)

async def make_request(messages: List[Dict[str, str]], temperature: float = 0.3) -> str:
    key = os.getenv("GROK_API_KEY")
    if not key:
        raise Exception("AI service key not found in environment")

    # Handle Groq (gsk_...) or X.AI (xai-...)
    is_groq = key.startswith("gsk_")
    url = "https://api.groq.com/openai/v1/chat/completions" if is_groq else "https://api.x.ai/v1/chat/completions"
    model = "llama-3.3-70b-versatile" if is_groq else "grok-2"
    
    print(f"🚀 [AI] Sending request to {'Groq' if is_groq else 'X.AI'} (model: {model})...")
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                print(f"❌ [AI] Error response: {response.status_code} - {response.text}")
                response.raise_for_status()
            
            result = response.json()
            print(f"✅ [AI] Response received from {'Groq' if is_groq else 'X.AI'}")
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ [AI] API error: {e}")
        raise e

def parse_json_response(text: str) -> Dict[str, Any]:
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
            print(f"❌ [AI] JSON parse error: {e} | Text: {cleaned_text[:300]}...")
            raise Exception(f"Invalid JSON in AI response. The model returned: {cleaned_text[:50]}...")
    
    print(f"❌ [AI] No JSON found in response: {text[:300]}...")
    raise Exception("The AI model did not return a structured JSON response.")

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
    messages = [
        {"role": "system", "content": "You are an expert resume analyzer. Return ONLY valid JSON."},
        {"role": "user", "content": prompt}
    ]
    response = await make_request(messages)
    return parse_json_response(response)

async def generate_training_plan(role: str) -> Dict[str, Any]:
    prompt = f"""
    Create a detailed professional training plan for the role of "{role}".
    
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
          "difficulty": "Beginner|Intermediate|Advanced"
        }}
      ],
      "certifications": ["string", ...]
    }}
    """
    messages = [
        {"role": "system", "content": "You are an expert educational planner. Return ONLY valid JSON."},
        {"role": "user", "content": prompt}
    ]
    response = await make_request(messages, 0.5)
    return parse_json_response(response)

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
    
    Return ONLY a JSON object with this exact structure:
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
    messages = [
        {"role": "system", "content": "You are an expert interview evaluator. Return ONLY valid JSON."},
        {"role": "user", "content": prompt}
    ]
    response = await make_request(messages, 0.4)
    return parse_json_response(response)

async def generate_quiz(role_or_skill: str) -> Dict[str, Any]:
    prompt = f"""
    Generate a quiz with 10 multiple-choice questions for "{role_or_skill}".
    
    Return ONLY a JSON object with this exact structure:
    {{
      "questions": [
        {{
          "question": "string",
          "options": ["string", "string", "string", "string"],
          "correctAnswer": "string"
        }}
      ]
    }}
    """
    messages = [
        {"role": "system", "content": "You are an expert quiz generator. Return ONLY valid JSON."},
        {"role": "user", "content": prompt}
    ]
    response = await make_request(messages, 0.4)
    parsed = parse_json_response(response)
    
    # Ensure we return the correct structure for frontend
    if "questions" not in parsed:
        print(f"❌ Grok response missing 'questions' key: {list(parsed.keys())}")
        return {"questions": []}
    
    print(f"✅ Grok generated {len(parsed.get('questions', []))} questions")
    return parsed

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
    messages = [
        {"role": "system", "content": "You are an expert interview coach. Return ONLY valid JSON with exactly 10 questions total."},
        {"role": "user", "content": prompt}
    ]
    response = await make_request(messages, 0.5)
    return parse_json_response(response)
