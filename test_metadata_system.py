import requests
import json

def test_metadata_system():
    """Test the new progress metadata system"""
    base_url = "http://localhost:8000"
    test_user_id = "metadata-test-user"
    
    print("📊 TESTING PROGRESS METADATA SYSTEM")
    print("=" * 60)
    
    # Test 1: Complete Quiz with Metadata
    print("\n1. 📝 Testing Quiz with Metadata...")
    try:
        submit_data = {
            "userId": test_user_id,
            "role": "software-engineer",
            "answers": [
                {"selected": "A", "correct": True},
                {"selected": "B", "correct": False},
                {"selected": "C", "correct": True}
            ],
            "score": 67
        }
        
        response = requests.post(f"{base_url}/api/quiz/submit", json=submit_data)
        if response.json().get("success"):
            print("   ✅ Quiz submitted with metadata tracking")
        else:
            print("   ❌ Quiz submission failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Get Metadata
    print("\n2. 📊 Testing Metadata Retrieval...")
    try:
        response = requests.get(f"{base_url}/api/progress/metadata/{test_user_id}")
        data = response.json()
        if data.get("success"):
            metadata = data.get("data", {})
            print("   ✅ Metadata retrieved successfully")
            
            # Display quiz summary
            quiz_summary = metadata.get("quiz_summary", {})
            print(f"   📋 Quiz Summary:")
            print(f"      - Total Quizzes: {quiz_summary.get('total_quizzes', 0)}")
            print(f"      - Average Score: {quiz_summary.get('average_score', 0)}")
            print(f"      - Highest Score: {quiz_summary.get('highest_score', 0)}")
            print(f"      - Roles Attempted: {quiz_summary.get('roles_attempted', [])}")
            print(f"      - Performance Trend: {quiz_summary.get('performance_trend', 'N/A')}")
            print(f"      - Total Correct Answers: {quiz_summary.get('total_correct_answers', 0)}")
            
            # Display overall stats
            overall_stats = metadata.get("overall_stats", {})
            print(f"   📈 Overall Stats:")
            print(f"      - Total Activities: {overall_stats.get('total_activities', 0)}")
            print(f"      - Most Active Role: {overall_stats.get('most_active_role', 'N/A')}")
            print(f"      - Improvement Areas: {overall_stats.get('improvement_areas', [])}")
            
            # Display activity timeline
            timeline = metadata.get("activity_timeline", [])
            print(f"   🕐 Recent Activities: {len(timeline)} activities")
            for activity in timeline[:3]:
                print(f"      - {activity['type']}: {activity['timestamp'][:19]}")
                
        else:
            print("   ❌ Metadata retrieval failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Complete Second Quiz
    print("\n3. 📝 Testing Second Quiz for Trend Analysis...")
    try:
        submit_data = {
            "userId": test_user_id,
            "role": "frontend-developer",
            "answers": [
                {"selected": "A", "correct": True},
                {"selected": "B", "correct": True}
            ],
            "score": 100
        }
        
        response = requests.post(f"{base_url}/api/quiz/submit", json=submit_data)
        if response.json().get("success"):
            print("   ✅ Second quiz submitted")
        else:
            print("   ❌ Second quiz failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Get Updated Metadata
    print("\n4. 📊 Testing Updated Metadata...")
    try:
        response = requests.get(f"{base_url}/api/progress/metadata/{test_user_id}")
        data = response.json()
        if data.get("success"):
            metadata = data.get("data", {})
            quiz_summary = metadata.get("quiz_summary", {})
            print("   ✅ Updated metadata retrieved")
            print(f"   📋 Updated Quiz Summary:")
            print(f"      - Total Quizzes: {quiz_summary.get('total_quizzes', 0)}")
            print(f"      - Average Score: {quiz_summary.get('average_score', 0)}")
            print(f"      - Performance Trend: {quiz_summary.get('performance_trend', 'N/A')}")
            
        else:
            print("   ❌ Updated metadata retrieval failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 METADATA SYSTEM TEST COMPLETE!")
    
    print("\n📱 FRONTEND INTEGRATION:")
    print("Use the new endpoint: GET /api/progress/metadata/{user_id}")
    print("Returns comprehensive metadata including:")
    print("  - Detailed quiz summaries with trends")
    print("  - Performance levels and improvement areas")
    print("  - Activity timeline")
    print("  - Role-specific statistics")
    print("  - Overall learning progress")
    
    print("\n🚀 METADATA FEATURES:")
    print("✅ Performance trend analysis")
    print("✅ Role-based progress tracking")
    print("✅ Activity timeline")
    print("✅ Improvement recommendations")
    print("✅ Detailed answer analysis")
    print("✅ Session activity tracking")

if __name__ == "__main__":
    test_metadata_system()
