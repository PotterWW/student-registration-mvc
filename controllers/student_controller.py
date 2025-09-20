# controllers/student_controller.py
from models.database_manager import DatabaseManager
from typing import List, Dict, Tuple

class StudentController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_student_profile(self, student_id: str) -> Dict:
        """Get student profile information"""
        return self.db_manager.get_student_by_id(student_id)
    
    def get_student_registered_subjects(self, student_id: str) -> List[Dict]:
        """Get all subjects the student has registered for"""
        return self.db_manager.get_student_registered_subjects(student_id)
    
    def get_available_subjects(self, student_id: str) -> List[Dict]:
        """Get subjects available for the student to register"""
        available_subjects = self.db_manager.get_available_subjects_for_student(student_id)
        
        # Add prerequisite check status for each subject
        for subject in available_subjects:
            can_register, message = self.db_manager.check_prerequisite(student_id, subject['subject_code'])
            subject['can_register'] = can_register
            subject['prerequisite_status'] = message
        
        return available_subjects
    
    def register_for_subject(self, student_id: str, subject_code: str) -> Tuple[bool, str]:
        """Register student for a subject"""
        return self.db_manager.register_subject(student_id, subject_code)
    
    def check_prerequisite(self, student_id: str, subject_code: str) -> Tuple[bool, str]:
        """Check if student meets prerequisite requirements"""
        return self.db_manager.check_prerequisite(student_id, subject_code)
    
    def get_student_gpa(self, student_id: str) -> float:
        """Calculate student's GPA based on completed subjects"""
        registered_subjects = self.get_student_registered_subjects(student_id)
        
        if not registered_subjects:
            return 0.0
        
        grade_points = {
            'A': 4.0, 'B+': 3.5, 'B': 3.0, 'C+': 2.5, 
            'C': 2.0, 'D+': 1.5, 'D': 1.0, 'F': 0.0
        }
        
        total_points = 0.0
        total_credits = 0
        
        for subject in registered_subjects:
            if subject['grade'] in grade_points:
                points = grade_points[subject['grade']] * subject['credits']
                total_points += points
                total_credits += subject['credits']
        
        return total_points / total_credits if total_credits > 0 else 0.0
    
    def get_completed_credits(self, student_id: str) -> int:
        """Get total credits completed by student"""
        registered_subjects = self.get_student_registered_subjects(student_id)
        
        total_credits = 0
        for subject in registered_subjects:
            if subject['grade'] not in ['F', 'IP']:
                total_credits += subject['credits']
        
        return total_credits
