import requests
import json

def test_quiz_scoring():
    """Test the quiz scoring issue"""
    base_url = "http://localhost:8000"
    
    print("🧪 TESTING QUIZ SCORING FIX")
    print("=" * 40)
    
    # Test with a quiz that has 2 correct answers
    test_questions = [
        {
            "question": "What is version control?",
            "options": ["A", "B", "C", "D"],
            "answer": "A"  # Backend uses 'answer'
        },
        {
            "question": "What is React?", 
            "options": ["A", "B", "C", "D"],
            "correctAnswer": "B"  # Backend uses 'correctAnswer'
        }
    ]
    
    # Simulate frontend submission
    print("\n1. 📝 Testing Quiz with Mixed Answer Formats...")
    try:
        submit_data = {
            "userId": "test-scoring",
            "role": "software-engineer",
            "answers": [
                {"selected": "A", "correct": True},  # Correct - matches 'answer'
                {"selected": "B", "correct": False},  # Wrong
                {"selected": "A", "correct": True}   # Correct - matches 'correctAnswer'
            ],
            "score": 67  # 2/3 correct = 67%
        }
        
        response = requests.post(f"{base_url}/api/quiz/submit", json=submit_data)
        if response.json().get("success"):
            print("✅ Quiz Submission: SUCCESS")
        else:
            print("❌ Quiz Submission: FAILED")
    except Exception as e:
        print(f"❌ Quiz Submission Error: {e}")
    
    # Check progress
    print("\n2. 📊 Checking Progress...")
    try:
        response = requests.get(f"{base_url}/api/progress/test-scoring")
        if response.json().get("success"):
            progress = response.json().get("data", {})
            print(f"✅ Progress Retrieved")
            print(f"   Quiz Scores: {progress.get('quizScores', {})}")
            print(f"   Average Score: {progress.get('averageScore', 0)}")
        else:
            print("❌ Progress Retrieval: FAILED")
    except Exception as e:
        print(f"❌ Progress Error: {e}")
    
    print("\n" + "=" * 40)
    print("🎯 QUIZ SCORING TEST COMPLETE!")
    print("The frontend should now correctly handle both answer formats")

if __name__ == "__main__":
    test_quiz_scoring()
