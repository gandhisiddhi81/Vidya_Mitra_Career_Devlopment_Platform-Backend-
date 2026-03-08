"""
Progress Metadata System for VidyaMitra 2.0
Tracks detailed metadata for all user activities
"""

import json
from datetime import datetime
from typing import Dict, List, Any

class ProgressMetadata:
    def __init__(self):
        self._metadata = {}
    
    def add_quiz_metadata(self, user_id: str, role: str, score: float, answers: List[Dict], time_taken: int = None):
        """Add detailed quiz metadata"""
        if user_id not in self._metadata:
            self._metadata[user_id] = {
                "quizzes": [],
                "interviews": [],
                "resume": [],
                "training": [],
                "sessions": []
            }
        
        quiz_metadata = {
            "type": "quiz",
            "role": role,
            "score": score,
            "total_questions": len(answers),
            "correct_answers": sum(1 for a in answers if a.get("correct", False)),
            "incorrect_answers": sum(1 for a in answers if not a.get("correct", False)),
            "time_taken_seconds": time_taken,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "performance_level": self._get_performance_level(score),
            "answers_summary": [
                {
                    "question_index": i,
                    "selected": a.get("selected", ""),
                    "correct": a.get("correct", False)
                } for i, a in enumerate(answers)
            ]
        }
        
        self._metadata[user_id]["quizzes"].append(quiz_metadata)
        print(f"📊 [Metadata] Added quiz metadata for {user_id}: {score}% ({role})")
    
    def add_interview_metadata(self, user_id: str, role: str, questions: List[str], answers: List[str], feedback: Dict):
        """Add detailed interview metadata"""
        if user_id not in self._metadata:
            self._metadata[user_id] = {
                "quizzes": [],
                "interviews": [],
                "resume": [],
                "training": [],
                "sessions": []
            }
        
        interview_metadata = {
            "type": "interview",
            "role": role,
            "questions_count": len(questions),
            "answers_count": len([a for a in answers if a.strip()]),
            "overall_score": feedback.get("overallScore", 0),
            "overall_feedback": feedback.get("overallFeedback", ""),
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "performance_level": self._get_performance_level(feedback.get("overallScore", 0)),
            "questions_answered": len([a for a in answers if a.strip()]),
            "feedback_summary": {
                "strengths": feedback.get("strengths", []),
                "improvements": feedback.get("improvements", []),
                "recommendations": feedback.get("recommendations", [])
            }
        }
        
        self._metadata[user_id]["interviews"].append(interview_metadata)
        print(f"🎭 [Metadata] Added interview metadata for {user_id}: {feedback.get('overallScore', 0)}% ({role})")
    
    def add_resume_metadata(self, user_id: str, file_name: str, score: int, analysis: Dict):
        """Add detailed resume metadata"""
        if user_id not in self._metadata:
            self._metadata[user_id] = {
                "quizzes": [],
                "interviews": [],
                "resume": [],
                "training": [],
                "sessions": []
            }
        
        resume_metadata = {
            "type": "resume",
            "file_name": file_name,
            "score": score,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "performance_level": self._get_performance_level(score),
            "analysis_summary": {
                "strengths_count": len(analysis.get("strengths", [])),
                "improvements_count": len(analysis.get("improvements", [])),
                "recommendations_count": len(analysis.get("recommendations", [])),
                "key_skills": analysis.get("key_skills", []),
                "experience_level": analysis.get("experience_level", "Unknown")
            }
        }
        
        self._metadata[user_id]["resume"].append(resume_metadata)
        print(f"📄 [Metadata] Added resume metadata for {user_id}: {score}% ({file_name})")
    
    def add_session_metadata(self, user_id: str, activity: str, details: Dict = None):
        """Add session activity metadata"""
        if user_id not in self._metadata:
            self._metadata[user_id] = {
                "quizzes": [],
                "interviews": [],
                "resume": [],
                "training": [],
                "sessions": []
            }
        
        session_metadata = {
            "activity": activity,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "details": details or {}
        }
        
        self._metadata[user_id]["sessions"].append(session_metadata)
        print(f"🕐 [Metadata] Added session metadata for {user_id}: {activity}")
    
    def get_user_metadata(self, user_id: str) -> Dict:
        """Get all metadata for a user"""
        return self._metadata.get(user_id, {
            "quizzes": [],
            "interviews": [],
            "resume": [],
            "training": [],
            "sessions": []
        })
    
    def get_progress_summary(self, user_id: str) -> Dict:
        """Get comprehensive progress summary with metadata"""
        metadata = self.get_user_metadata(user_id)
        
        # Quiz summary
        quizzes = metadata["quizzes"]
        quiz_scores = [q["score"] for q in quizzes]
        quiz_summary = {
            "total_quizzes": len(quizzes),
            "average_score": round(sum(quiz_scores) / len(quiz_scores), 1) if quiz_scores else 0,
            "highest_score": max(quiz_scores) if quiz_scores else 0,
            "lowest_score": min(quiz_scores) if quiz_scores else 0,
            "most_recent_quiz": quizzes[-1] if quizzes else None,
            "roles_attempted": list(set(q["role"] for q in quizzes)),
            "performance_trend": self._calculate_trend(quiz_scores),
            "total_correct_answers": sum(q["correct_answers"] for q in quizzes),
            "total_questions_attempted": sum(q["total_questions"] for q in quizzes)
        }
        
        # Interview summary
        interviews = metadata["interviews"]
        interview_scores = [i["overall_score"] for i in interviews]
        interview_summary = {
            "total_interviews": len(interviews),
            "average_score": round(sum(interview_scores) / len(interview_scores), 1) if interview_scores else 0,
            "highest_score": max(interview_scores) if interview_scores else 0,
            "roles_practiced": list(set(i["role"] for i in interviews)),
            "most_recent_interview": interviews[-1] if interviews else None,
            "total_questions_answered": sum(i["questions_answered"] for i in interviews)
        }
        
        # Resume summary
        resumes = metadata["resume"]
        resume_summary = {
            "total_uploads": len(resumes),
            "latest_score": resumes[-1]["score"] if resumes else 0,
            "files_analyzed": [r["file_name"] for r in resumes],
            "latest_analysis": resumes[-1] if resumes else None
        }
        
        # Activity timeline
        all_activities = []
        for quiz in quizzes:
            all_activities.append({"type": "quiz", "timestamp": quiz["timestamp"], "data": quiz})
        for interview in interviews:
            all_activities.append({"type": "interview", "timestamp": interview["timestamp"], "data": interview})
        for resume in resumes:
            all_activities.append({"type": "resume", "timestamp": resume["timestamp"], "data": resume})
        
        # Sort by timestamp
        all_activities.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "user_id": user_id,
            "quiz_summary": quiz_summary,
            "interview_summary": interview_summary,
            "resume_summary": resume_summary,
            "activity_timeline": all_activities[:10],  # Last 10 activities
            "overall_stats": {
                "total_activities": len(quizzes) + len(interviews) + len(resumes),
                "last_activity": all_activities[0]["timestamp"] if all_activities else None,
                "most_active_role": self._get_most_active_role(quizzes, interviews),
                "improvement_areas": self._get_improvement_areas(quizzes, interviews)
            }
        }
    
    def _get_performance_level(self, score: float) -> str:
        """Get performance level based on score"""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Average"
        elif score >= 60:
            return "Below Average"
        else:
            return "Needs Improvement"
    
    def _calculate_trend(self, scores: List[float]) -> str:
        """Calculate performance trend"""
        if len(scores) < 2:
            return "Insufficient Data"
        
        recent = scores[-3:] if len(scores) >= 3 else scores
        if len(recent) < 2:
            return "Insufficient Data"
        
        improvement = recent[-1] - recent[0]
        if improvement > 10:
            return "Improving"
        elif improvement < -10:
            return "Declining"
        else:
            return "Stable"
    
    def _get_most_active_role(self, quizzes: List, interviews: List) -> str:
        """Get the most practiced role"""
        all_roles = [q["role"] for q in quizzes] + [i["role"] for i in interviews]
        if not all_roles:
            return "None"
        
        from collections import Counter
        role_counts = Counter(all_roles)
        return role_counts.most_common(1)[0][0]
    
    def _get_improvement_areas(self, quizzes: List, interviews: List) -> List[str]:
        """Get areas that need improvement"""
        areas = []
        
        # Check quiz performance
        quiz_scores = [q["score"] for q in quizzes]
        if quiz_scores and sum(quiz_scores) / len(quiz_scores) < 70:
            areas.append("Quiz Performance")
        
        # Check interview performance
        interview_scores = [i["overall_score"] for i in interviews]
        if interview_scores and sum(interview_scores) / len(interview_scores) < 70:
            areas.append("Interview Performance")
        
        # Check consistency
        if len(quiz_scores) > 2:
            if max(quiz_scores) - min(quiz_scores) > 30:
                areas.append("Consistency")
        
        return areas if areas else ["No specific areas identified"]

# Global metadata instance
progress_metadata = ProgressMetadata()
