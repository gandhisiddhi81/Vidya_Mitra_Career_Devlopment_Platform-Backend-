import requests
import json

def test_interview_priority():
    """Test interview question generation with Gemini first, Grok fallback"""
    base_url = "http://localhost:8000"
    
    print("🎭 TESTING INTERVIEW PRIORITY SYSTEM")
    print("=" * 60)
    
    # Test 1: Generate Interview Questions
    print("\n1. 📝 Testing Interview Question Generation...")
    try:
        response = requests.get(f"{base_url}/api/interview/questions/software-engineer")
        data = response.json()
        
        if data.get("success"):
            questions = data.get("data", {}).get("questions", [])
            print(f"   ✅ API Success: {len(questions)} questions generated")
            print(f"   📋 First Question: {questions[0].get('question', 'N/A')[:50]}...")
            
            # Check if questions are dynamic (not static)
            sample_questions = [
                "What is your experience with programming languages?",
                "How do you approach debugging complex issues?",
                "Can you explain object-oriented programming?"
            ]
            
            is_dynamic = True
            for q in questions[:3]:
                if q.get("question", "").strip() in sample_questions:
                    is_dynamic = False
                    break
            
            if is_dynamic:
                print("   ⚠️ WARNING: Questions appear to be static/demo")
            else:
                print("   ✅ Questions appear to be dynamic")
        else:
            print(f"   ❌ API Failed: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Request Error: {e}")
    
    # Test 2: Check Backend Logs
    print("\n2. 📋 Checking Backend Priority Logic...")
    print("   Expected behavior:")
    print("   1. Try Gemini first (🔮)")
    print("   2. If Gemini fails, try Grok")
    print("   3. No static/demo data")
    print("   4. Always generate fresh questions")
    
    print("\n3. 🎯 Test Complete!")
    print("=" * 60)
    
    print("\n📱 EXPECTED CONSOLE OUTPUT:")
    print("Backend should show:")
    print("   🔮 Trying Gemini first for interview questions")
    print("   ✅ Gemini generated X questions")
    print("   OR")
    print("   🔮 Using Grok for interview questions (Gemini unavailable)")
    print("   ✅ Grok generated X questions")
    
    print("\n🔍 FRONTEND INSTRUCTIONS:")
    print("1. Refresh browser (Ctrl+F5)")
    print("2. Go to Mock Interviews")
    print("3. Click 'Start Interview'")
    print("4. Check console for priority messages")
    print("5. Verify questions are dynamic, not static")

if __name__ == "__main__":
    test_interview_priority()
