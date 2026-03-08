import asyncio
import json
import requests

async def test_complete_system():
    """Test all major APIs to ensure complete functionality"""
    base_url = "http://localhost:8000"
    test_user_id = "test-user-complete"
    
    print("🧪 TESTING VIDYAMITRA 2.0 COMPLETE SYSTEM")
    print("=" * 50)
    
    # Test 1: Quiz Generation
    print("\n1. 📝 Testing Quiz Generation...")
    try:
        response = requests.get(f"{base_url}/api/quiz/software-engineer")
        data = response.json()
        if data.get("success") and data.get("data", {}).get("questions"):
            questions = data["data"]["questions"]
            print(f"✅ Quiz Generation: SUCCESS ({len(questions)} questions)")
            print(f"   Sample Question: {questions[0].get('question', 'N/A')[:50]}...")
        else:
            print("❌ Quiz Generation: FAILED - No questions returned")
    except Exception as e:
        print(f"❌ Quiz Generation: ERROR - {e}")
    
    # Test 2: Quiz Submission & Progress Tracking
    print("\n2. 📊 Testing Quiz Submission & Progress...")
    try:
        submit_data = {
            "userId": test_user_id,
            "role": "software-engineer",
            "answers": [
                {"selected": "A", "correct": True},
                {"selected": "B", "correct": False},
                {"selected": "C", "correct": True}
            ],
            "score": 70
        }
        response = requests.post(f"{base_url}/api/quiz/submit", json=submit_data)
        if response.json().get("success"):
            print("✅ Quiz Submission: SUCCESS")
        else:
            print("❌ Quiz Submission: FAILED")
    except Exception as e:
        print(f"❌ Quiz Submission: ERROR - {e}")
    
    # Test 3: Progress Retrieval
    print("\n3. 📈 Testing Progress Retrieval...")
    try:
        response = requests.get(f"{base_url}/api/progress/{test_user_id}")
        data = response.json()
        if data.get("success"):
            progress = data.get("data", {})
            print(f"✅ Progress Retrieval: SUCCESS")
            print(f"   Quizzes Completed: {progress.get('quizzesCompleted', 0)}")
            print(f"   Average Score: {progress.get('averageScore', 0)}")
            print(f"   Quiz Scores: {progress.get('quizScores', [])}")
        else:
            print("❌ Progress Retrieval: FAILED")
    except Exception as e:
        print(f"❌ Progress Retrieval: ERROR - {e}")
    
    # Test 4: Interview Questions
    print("\n4. 🎭 Testing Interview Questions...")
    try:
        response = requests.get(f"{base_url}/api/interview/questions/software-engineer")
        data = response.json()
        if data.get("success") and data.get("data", {}).get("questions"):
            questions = data["data"]["questions"]
            print(f"✅ Interview Questions: SUCCESS ({len(questions)} questions)")
            print(f"   Sample Question: {questions[0].get('question', 'N/A')[:50]}...")
        else:
            print("❌ Interview Questions: FAILED - No questions returned")
    except Exception as e:
        print(f"❌ Interview Questions: ERROR - {e}")
    
    # Test 5: Interview Feedback
    print("\n5. 🗣️ Testing Interview Feedback...")
    try:
        feedback_data = {
            "userId": test_user_id,
            "role": "software-engineer",
            "answers": [
                {"question": "What is your experience?", "text": "I have 5 years of experience"}
            ]
        }
        response = requests.post(f"{base_url}/api/interview/feedback", json=feedback_data)
        data = response.json()
        if data.get("success"):
            result = data.get("data", {})
            print("✅ Interview Feedback: SUCCESS")
            print(f"   Overall Score: {result.get('overallScore', 'N/A')}")
            print(f"   Feedback: {result.get('overallFeedback', 'N/A')[:50]}...")
        else:
            print("❌ Interview Feedback: FAILED")
    except Exception as e:
        print(f"❌ Interview Feedback: ERROR - {e}")
    
    # Test 6: Resume Analysis
    print("\n6. 📄 Testing Resume Analysis...")
    try:
        resume_data = {
            "text": "Experienced software engineer with 5 years in Python and JavaScript",
            "fileName": "test_resume.txt"
        }
        response = requests.post(f"{base_url}/api/resume/analyze", json=resume_data)
        data = response.json()
        if data.get("success"):
            result = data.get("data", {})
            print("✅ Resume Analysis: SUCCESS")
            print(f"   Score: {result.get('score', 'N/A')}")
            print(f"   Strengths: {len(result.get('strengths', []))}")
        else:
            print("❌ Resume Analysis: FAILED")
    except Exception as e:
        print(f"❌ Resume Analysis: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print("🎯 SYSTEM TEST COMPLETE!")
    print("If all tests show SUCCESS, your VidyaMitra 2.0 is fully functional!")

if __name__ == "__main__":
    asyncio.run(test_complete_system())
