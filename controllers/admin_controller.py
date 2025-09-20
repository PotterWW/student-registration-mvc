# controllers/admin_controller.py
from models.database_manager import DatabaseManager
from typing import List, Dict

class AdminController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_all_students(self) -> List[Dict]:
        """Get all students for admin view"""
        return self.db_manager.get_all_students()
    
    def search_students(self, search_term: str = "", school_filter: str = "", sort_by: str = "name") -> List[Dict]:
        """Search and filter students"""
        return self.db_manager.search_students(search_term, school_filter, sort_by)
    
    def get_schools(self) -> List[str]:
        """Get list of all schools for filtering"""
        return self.db_manager.get_schools()
    
    def get_student_details(self, student_id: str) -> Dict:
        """Get detailed student information"""
        return self.db_manager.get_student_by_id(student_id)
    
    def get_student_registered_subjects(self, student_id: str) -> List[Dict]:
        """Get student's registered subjects"""
        return self.db_manager.get_student_registered_subjects(student_id)
    
    def get_all_subjects(self) -> List[Dict]:
        """Get all subjects for grade entry"""
        return self.db_manager.get_all_subjects()
    
    def get_subject_registrations(self, subject_code: str) -> List[Dict]:
        """Get all students registered for a specific subject"""
        return self.db_manager.get_subject_registrations(subject_code)
    
    def update_student_grade(self, student_id: str, subject_code: str, grade: str) -> bool:
        """Update student's grade for a subject"""
        valid_grades = ['A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F', 'IP']
        
        if grade not in valid_grades:
            return False
        
        return self.db_manager.update_grade(student_id, subject_code, grade)
    
    def get_registration_statistics(self) -> Dict:
        """Get statistics about registrations"""
        subjects = self.get_all_subjects()
        students = self.get_all_students()
        
        total_registrations = 0
        subject_registration_counts = {}
        
        for subject in subjects:
            registrations = self.get_subject_registrations(subject['subject_code'])
            count = len(registrations)
            subject_registration_counts[subject['subject_code']] = count
            total_registrations += count
        
        stats = {
            'total_subjects': len(subjects),
            'total_students': len(students),
            'total_registrations': total_registrations,
            'subject_registration_counts': subject_registration_counts
        }
        
        return stats
