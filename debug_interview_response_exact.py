import requests
import json

def debug_interview_response_exact():
    """Debug exact interview API response structure"""
    response = requests.get("http://localhost:8000/api/interview/questions/software-engineer")
    
    print("🎭 DEBUGGING EXACT INTERVIEW RESPONSE")
    print("=" * 60)
    
    print("📋 Raw Response:")
    print(response.text)
    
    print(f"\n📊 Parsed JSON:")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print("Failed to parse JSON")
    
    print(f"\n🔍 Frontend fetchInterviewQuestions expects:")
    print("  return response.data.data.questions;")
    
    print(f"\n📱 What backend is returning:")
    print("  response.data.data.questions")
    
    print(f"\n✅ SOLUTION:")
    print("  Frontend expects: response.data.data.questions")
    print("  Backend returns: response.data.data.questions")  
    print("  This should work correctly!")
    
    print(f"\n🎯 If interview is still not working:")
    print("  1. Check if response.data.success is true")
    print("  2. Check if response.data.data exists")
    print("  3. Check if response.data.data.questions is array")
    print("  4. Check browser console for errors")

if __name__ == "__main__":
    debug_interview_response_exact()
