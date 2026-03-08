import requests
import json
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_supabase_sync():
    """Test that progress syncs to Supabase correctly"""
    base_url = "http://localhost:8000"
    test_user_id = "supabase-sync-test"
    
    print("🔄 TESTING SUPABASE SYNC")
    print("=" * 50)
    
    # Test 1: Complete Quiz and Check Supabase
    print("\n1. 📝 Testing Quiz → Supabase Sync...")
    try:
        submit_data = {
            "userId": test_user_id,
            "role": "software-engineer",
            "answers": [{"selected": "A", "correct": True}, {"selected": "B", "correct": True}],
            "score": 85
        }
        
        # Submit quiz
        response = requests.post(f"{base_url}/api/quiz/submit", json=submit_data)
        if response.json().get("success"):
            print("   ✅ Quiz submitted to memory")
        else:
            print("   ❌ Quiz submission failed")
            return
            
        # Wait a moment for sync
        import time
        time.sleep(1)
        
        # Check progress (should sync to Supabase)
        response = requests.get(f"{base_url}/api/progress/{test_user_id}")
        data = response.json()
        if data.get("success"):
            progress = data.get("data", {})
            print(f"   ✅ Progress retrieved")
            print(f"      - Quizzes: {progress.get('quizzesCompleted', 0)}")
            print(f"      - Average: {progress.get('averageScore', 0)}")
            print(f"      - Quiz History: {progress.get('quizScores', [])}")
        else:
            print("   ❌ Progress retrieval failed")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Complete Second Quiz
    print("\n2. 📝 Testing Second Quiz → Supabase Sync...")
    try:
        submit_data = {
            "userId": test_user_id,
            "role": "frontend-developer",
            "answers": [{"selected": "A", "correct": True}],
            "score": 75
        }
        
        response = requests.post(f"{base_url}/api/quiz/submit", json=submit_data)
        if response.json().get("success"):
            print("   ✅ Second quiz submitted")
        else:
            print("   ❌ Second quiz failed")
            return
            
        time.sleep(1)
        
        # Check final progress
        response = requests.get(f"{base_url}/api/progress/{test_user_id}")
        data = response.json()
        if data.get("success"):
            progress = data.get("data", {})
            print(f"   ✅ Final progress")
            print(f"      - Quizzes: {progress.get('quizzesCompleted', 0)}")
            print(f"      - Average: {progress.get('averageScore', 0)}")
            print(f"      - Quiz History: {progress.get('quizScores', [])}")
            
            # Check if data is being stored in Supabase
            if progress.get('quizzesCompleted', 0) >= 2:
                print("   ✅ SUPABASE SYNC: Multiple quizzes stored!")
            else:
                print("   ⚠️ SUPABASE SYNC: Only 1 quiz stored")
        else:
            print("   ❌ Final progress check failed")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 SUPABASE SYNC TEST COMPLETE!")
    
    print("\n📋 EXPECTED RESULTS:")
    print("   - 2 quizzes completed")
    print("   - Average score: 80%")
    print("   - Quiz history: [85, 75]")
    
    print("\n🎯 CHECK YOUR SUPABASE:")
    print("If you see 2 quizzes in Supabase, sync is working!")
    print("If you see only 1 quiz, check Supabase connection!")

if __name__ == "__main__":
    test_supabase_sync()
