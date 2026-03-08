import os
import asyncio
from dotenv import load_dotenv
load_dotenv() # MUST be before service import

from services import grok_service

async def test_resume_analysis():
    resume_text = """
    John Doe
    Software Engineer
    Experience:
    - 5 years at TechCorp
    - Skills: Python, React, AWS, Docker
    Education: BS in CS
    """
    print(f"Testing Groq analysis with key: {os.getenv('GROK_API_KEY')[:10]}...")
    try:
        result = await grok_service.analyze_resume(resume_text)
        print("✅ Success!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_resume_analysis())
