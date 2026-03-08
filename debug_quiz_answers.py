import requests
import json

def debug_quiz_answers():
    """Debug quiz answer format"""
    response = requests.get("http://localhost:8000/api/quiz/software-engineer")
    data = response.json()
    
    print("🔍 DEBUGGING QUIZ ANSWER FORMAT")
    print("=" * 50)
    
    if data.get('success') and data.get('data'):
        questions = data['data']['questions']
        for i, q in enumerate(questions[:3]):  # First 3 questions
            print(f"\nQuestion {i+1}:")
            print(f"  Question: {q.get('question', 'N/A')}")
            print(f"  Options: {q.get('options', [])}")
            print(f"  Correct Answer: '{q.get('correctAnswer', 'MISSING')}'")
            print(f"  Expected Selection: Should match the correct option text")
            
            # Check if correctAnswer matches any option
            options = q.get('options', [])
            correct_answer = q.get('correctAnswer', '')
            if correct_answer in options:
                print(f"  ✅ Correct answer found in options at index {options.index(correct_answer)}")
                print(f"  ✅ User should select: {['A', 'B', 'C', 'D'][options.index(correct_answer)]}")
            else:
                print(f"  ❌ Correct answer NOT found in options!")
                print(f"  ❌ This is why all answers appear wrong!")
    
    print("\n" + "=" * 50)
    print("🎯 DEBUG COMPLETE!")

if __name__ == "__main__":
    debug_quiz_answers()
