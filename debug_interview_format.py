import requests
import json

def debug_interview_format():
    """Debug interview question format"""
    response = requests.get("http://localhost:8000/api/interview/questions/software-engineer")
    data = response.json()
    
    print("🔍 DEBUGGING INTERVIEW QUESTION FORMAT")
    print("=" * 50)
    
    if data.get('success') and data.get('data'):
        questions = data['data']['questions']
        print(f"Questions Count: {len(questions)}")
        print(f"Question Type: {type(questions[0]) if questions else 'N/A'}")
        
        for i, q in enumerate(questions[:3]):  # First 3 questions
            print(f"\nQuestion {i+1}:")
            print(f"  Raw: {q}")
            print(f"  Type: {type(q)}")
            
            if isinstance(q, str):
                print(f"  ✅ String format - Frontend should display this directly")
            elif isinstance(q, dict):
                print(f"  📋 Object format - Keys: {list(q.keys())}")
                if 'question' in q:
                    print(f"    Question Text: {q.get('question', 'N/A')}")
                if 'category' in q:
                    print(f"    Category: {q.get('category', 'N/A')}")
            else:
                print(f"  ❌ Unknown format")
    
    print("\n" + "=" * 50)
    print("🎯 DEBUG COMPLETE!")

if __name__ == "__main__":
    debug_interview_format()
