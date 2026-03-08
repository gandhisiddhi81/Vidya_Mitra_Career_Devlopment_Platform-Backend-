import requests
import json

def debug_interview_frontend():
    """Debug interview API response format"""
    response = requests.get("http://localhost:8000/api/interview/questions/software-engineer")
    data = response.json()
    
    print("🎭 DEBUGGING INTERVIEW API RESPONSE")
    print("=" * 50)
    
    if data.get("success"):
        interview_data = data.get("data", {})
        questions = interview_data.get("questions", [])
        print(f"✅ API Response: SUCCESS")
        print(f"📋 Questions Count: {len(questions)}")
        print(f"🎭 Role: {interview_data.get('role', 'N/A')}")
        
        print(f"\n📝 Question Formats:")
        for i, q in enumerate(questions[:3]):  # First 3 questions
            print(f"   Question {i+1}:")
            print(f"      Type: {type(q)}")
            print(f"      Keys: {list(q.keys()) if isinstance(q, dict) else 'String'}")
            if isinstance(q, dict):
                print(f"      Question Text: {q.get('question', 'N/A')[:50]}...")
                print(f"      Category: {q.get('category', 'N/A')}")
            else:
                print(f"      Question Text: {str(q)[:50]}...")
        
        print(f"\n🔍 Frontend Expected Format:")
        print(f"   - Questions should be array of objects with 'question' key")
        print(f"   - Frontend should display: {{typeof question === 'string' ? question : question.question}}")
        print(f"   - Current fix handles both string and object formats")
        
    else:
        print("❌ API Response: FAILED")
    
    print("\n" + "=" * 50)
    print("🎯 DEBUG COMPLETE!")
    
    print("\n💡 FRONTEND ISSUE DIAGNOSIS:")
    print("If interview questions display but don't work:")
    print("1. Check if questions are being set in state")
    print("2. Check if interviewQuestions.length > 0")
    print("3. Check if interviewQuestions.map() is working")
    print("4. Check browser console for JavaScript errors")
    print("5. Check if interview submission is working")
    
    print("\n📱 FRONTEND DEBUGGING:")
    print("Add console.log to Dashboard.jsx:")
    print("console.log('Interview questions:', interviewQuestions)")
    print("console.log('Interview loading:', interviewLoading)")
    print("console.log('Interview error:', interviewError)")

if __name__ == "__main__":
    debug_interview_frontend()
