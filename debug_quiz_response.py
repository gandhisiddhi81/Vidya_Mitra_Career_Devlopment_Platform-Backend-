import requests
import json

def debug_quiz_response():
    """Debug the exact quiz API response format"""
    response = requests.get("http://localhost:8000/api/quiz/software-engineer")
    data = response.json()
    
    print("🔍 DEBUGGING QUIZ API RESPONSE")
    print("=" * 50)
    print(f"Status Code: {response.status_code}")
    print(f"Success: {data.get('success')}")
    print(f"Data Keys: {list(data.get('data', {}).keys())}")
    
    if data.get('success') and data.get('data'):
        quiz_data = data['data']
        print(f"Role: {quiz_data.get('role')}")
        print(f"Questions Count: {len(quiz_data.get('questions', []))}")
        
        questions = quiz_data.get('questions', [])
        if questions:
            print(f"First Question Structure: {json.dumps(questions[0], indent=2)}")
            
            # Check what the frontend expects
            print(f"\n📋 Frontend Expectations:")
            print(f"  - question: {questions[0].get('question', 'MISSING')}")
            print(f"  - options: {questions[0].get('options', 'MISSING')}")
            print(f"  - answer: {questions[0].get('answer', 'MISSING')}")
            print(f"  - correctAnswer: {questions[0].get('correctAnswer', 'MISSING')}")
        else:
            print("❌ No questions found!")
    else:
        print("❌ API response failed!")
    
    print("\n" + "=" * 50)
    print("🎯 DEBUG COMPLETE!")

if __name__ == "__main__":
    debug_quiz_response()
