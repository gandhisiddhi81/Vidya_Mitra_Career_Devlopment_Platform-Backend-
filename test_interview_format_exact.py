import requests
import json

def test_interview_exact_format():
    """Test exact interview API response format"""
    response = requests.get("http://localhost:8000/api/interview/questions/software-engineer")
    data = response.json()
    
    print("🎭 TESTING EXACT INTERVIEW FORMAT")
    print("=" * 50)
    
    print(f"Status Code: {response.status_code}")
    print(f"Success: {data.get('success')}")
    
    if data.get('success') and data.get('data'):
        interview_data = data['data']
        print(f"Role: {interview_data.get('role', 'N/A')}")
        
        questions = interview_data.get('questions', [])
        print(f"Questions Count: {len(questions)}")
        print(f"First Question Type: {type(questions[0]) if questions else 'None'}")
        
        print(f"\n📋 First Question Structure:")
        if questions:
            q = questions[0]
            print(f"Raw: {json.dumps(q, indent=2)}")
            print(f"Keys: {list(q.keys())}")
            print(f"Has 'question' key: {'question' in q}")
            print(f"Question text: {q.get('question', 'MISSING')}")
            
            # Test what frontend expects
            print(f"\n🔍 Frontend Compatibility Test:")
            if isinstance(q, str):
                print("✅ String format - Frontend should display directly")
            elif isinstance(q, dict) and 'question' in q:
                print("✅ Object format - Frontend should use q.question")
            else:
                print("❌ Unknown format - This is the problem!")
        
        print(f"\n📱 Frontend Expected:")
        print("1. fetchInterviewQuestions() should return array")
        print("2. setInterviewQuestions(data) should work")
        print("3. interviewQuestions.map() should iterate")
        print("4. typeof question === 'string' ? question : question.question")
        
    else:
        print("❌ API call failed")
    
    print("\n" + "=" * 50)
    print("🎯 FORMAT TEST COMPLETE!")

if __name__ == "__main__":
    test_interview_exact_format()
