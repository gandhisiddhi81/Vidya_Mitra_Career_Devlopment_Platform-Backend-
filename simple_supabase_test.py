import requests
import json
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_simple_supabase():
    """Simple test to check Supabase connection"""
    base_url = "http://localhost:8000"
    test_user_id = "simple-test-user"
    
    print("🔍 SIMPLE SUPABASE TEST")
    print("=" * 40)
    
    # Test 1: Direct progress check
    print("\n1. 📊 Testing Direct Progress API...")
    try:
        response = requests.get(f"{base_url}/api/progress/{test_user_id}")
        data = response.json()
        if data.get("success"):
            progress = data.get("data", {})
            print(f"   ✅ Progress API working")
            print(f"      - Quizzes: {progress.get('quizzesCompleted', 0)}")
            print(f"      - Average: {progress.get('averageScore', 0)}")
        else:
            print("   ❌ Progress API failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Simple quiz submission
    print("\n2. 📝 Testing Simple Quiz Submission...")
    try:
        submit_data = {
            "userId": test_user_id,
            "role": "software-engineer",
            "answers": [{"selected": "A", "correct": True}],
            "score": 90
        }
        
        response = requests.post(f"{base_url}/api/quiz/submit", json=submit_data)
        print(f"   Quiz submit response: {response.status_code}")
        
        if response.json().get("success"):
            print("   ✅ Quiz submitted successfully")
        else:
            print("   ❌ Quiz submission failed")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Check progress again
    print("\n3. 📊 Testing Progress After Quiz...")
    try:
        response = requests.get(f"{base_url}/api/progress/{test_user_id}")
        data = response.json()
        if data.get("success"):
            progress = data.get("data", {})
            print(f"   ✅ Progress after quiz:")
            print(f"      - Quizzes: {progress.get('quizzesCompleted', 0)}")
            print(f"      - Average: {progress.get('averageScore', 0)}")
            print(f"      - Quiz History: {progress.get('quizScores', [])}")
            
            if progress.get('quizzesCompleted', 0) > 0:
                print("   🎉 PROGRESS INCREMENTED!")
            else:
                print("   ⚠️ Progress not incremented")
        else:
            print("   ❌ Progress check failed")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("🎯 SIMPLE TEST COMPLETE!")
    
    print("\n💡 DIAGNOSIS:")
    print("If progress increments, Supabase sync is working")
    print("If not, check backend logs for Supabase errors")
    print("The issue might be in table structure or permissions")

if __name__ == "__main__":
    test_simple_supabase()
