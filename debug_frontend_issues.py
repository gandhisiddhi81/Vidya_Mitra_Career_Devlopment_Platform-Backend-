import requests
import json

def debug_frontend_apis():
    """Debug the exact API calls the frontend makes"""
    base_url = "http://localhost:8000"
    test_user_id = "test-debug-user"
    
    print("🔍 DEBUGGING FRONTEND API INTEGRATION")
    print("=" * 50)
    
    # Test 1: Simulate Quiz Completion (like frontend does)
    print("\n1. 📝 Simulating Quiz Completion...")
    try:
        submit_data = {
            "userId": test_user_id,
            "role": "software-engineer", 
            "answers": [
                {"selected": "A", "correct": True},
                {"selected": "B", "correct": False}
            ],
            "score": 80
        }
        response = requests.post(f"{base_url}/api/quiz/submit", json=submit_data)
        print(f"   Quiz Submit Response: {response.status_code}")
        print(f"   Response Body: {response.text[:200]}...")
    except Exception as e:
        print(f"   Quiz Submit Error: {e}")
    
    # Test 2: Check Progress (like frontend does)
    print("\n2. 📊 Checking Progress After Quiz...")
    try:
        response = requests.get(f"{base_url}/api/progress/{test_user_id}")
        data = response.json()
        print(f"   Progress Response: {response.status_code}")
        if data.get("success"):
            progress = data.get("data", {})
            print(f"   ✅ Progress Success: {json.dumps(progress, indent=2)}")
        else:
            print(f"   ❌ Progress Failed: {response.text}")
    except Exception as e:
        print(f"   Progress Error: {e}")
    
    # Test 3: Simulate Interview Completion (like frontend does)
    print("\n3. 🎭 Simulating Interview Completion...")
    try:
        interview_data = {
            "userId": test_user_id,
            "role": "software-engineer",
            "answers": [
                {"question": "What is your experience?", "text": "5 years of software engineering"}
            ]
        }
        response = requests.post(f"{base_url}/api/interview/feedback", json=interview_data)
        print(f"   Interview Submit Response: {response.status_code}")
        print(f"   Response Body: {response.text[:200]}...")
    except Exception as e:
        print(f"   Interview Submit Error: {e}")
    
    # Test 4: Check Progress Again (like frontend does)
    print("\n4. 📈 Checking Progress After Interview...")
    try:
        response = requests.get(f"{base_url}/api/progress/{test_user_id}")
        data = response.json()
        if data.get("success"):
            progress = data.get("data", {})
            print(f"   ✅ Final Progress: {json.dumps(progress, indent=2)}")
            print(f"   📊 Summary:")
            print(f"      - Quizzes Completed: {progress.get('quizzesCompleted', 0)}")
            print(f"      - Average Score: {progress.get('averageScore', 0)}")
            print(f"      - Interviews Completed: {progress.get('interviews_completed', 0)}")
        else:
            print(f"   ❌ Final Progress Failed: {response.text}")
    except Exception as e:
        print(f"   Final Progress Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 DEBUG COMPLETE!")
    print("Check if quiz scores and interview completion are being tracked properly")

if __name__ == "__main__":
    debug_frontend_apis()
