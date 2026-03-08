import requests
import json

def test_progress_increment():
    """Test that quiz progress increments correctly"""
    base_url = "http://localhost:8000"
    test_user_id = "progress-test-user"
    
    print("🧪 TESTING QUIZ PROGRESS INCREMENT")
    print("=" * 50)
    
    # Test 1: Complete First Quiz (Score: 80)
    print("\n1. 📝 Completing First Quiz (Score: 80)...")
    try:
        submit_data = {
            "userId": test_user_id,
            "role": "software-engineer",
            "answers": [{"selected": "A", "correct": True}, {"selected": "B", "correct": True}],
            "score": 80
        }
        response = requests.post(f"{base_url}/api/quiz/submit", json=submit_data)
        if response.json().get("success"):
            print("   ✅ First quiz submitted")
        else:
            print("   ❌ First quiz failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Check Progress After First Quiz
    print("\n2. 📊 Checking Progress After First Quiz...")
    try:
        response = requests.get(f"{base_url}/api/progress/{test_user_id}")
        data = response.json()
        if data.get("success"):
            progress = data.get("data", {})
            print(f"   ✅ Progress: {progress.get('quizzesCompleted', 0)} quizzes, {progress.get('averageScore', 0)} avg")
        else:
            print("   ❌ Progress check failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Complete Second Quiz (Score: 60)
    print("\n3. 📝 Completing Second Quiz (Score: 60)...")
    try:
        submit_data = {
            "userId": test_user_id,
            "role": "frontend-developer",
            "answers": [{"selected": "A", "correct": True}, {"selected": "C", "correct": True}],
            "score": 60
        }
        response = requests.post(f"{base_url}/api/quiz/submit", json=submit_data)
        if response.json().get("success"):
            print("   ✅ Second quiz submitted")
        else:
            print("   ❌ Second quiz failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Check Progress After Second Quiz
    print("\n4. 📊 Checking Progress After Second Quiz...")
    try:
        response = requests.get(f"{base_url}/api/progress/{test_user_id}")
        data = response.json()
        if data.get("success"):
            progress = data.get("data", {})
            print(f"   ✅ Progress: {progress.get('quizzesCompleted', 0)} quizzes, {progress.get('averageScore', 0)} avg")
            print(f"   ✅ Quiz History: {progress.get('quizScores', [])}")
        else:
            print("   ❌ Progress check failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 PROGRESS INCREMENT TEST COMPLETE!")
    
    expected_quizzes = 2
    expected_avg = round((80 + 60) / 2, 1)
    print(f"\n📋 Expected Results:")
    print(f"   - Quizzes Completed: {expected_quizzes}")
    print(f"   - Average Score: {expected_avg}")
    print(f"   - Quiz History: [80, 60]")
    
    print("\n🎯 TEST YOUR FRONTEND:")
    print("If you see 2 quizzes and 70% average, the fix is working!")
    print("If you see 1 quiz and old average, the fix needs debugging.")

if __name__ == "__main__":
    test_progress_increment()
