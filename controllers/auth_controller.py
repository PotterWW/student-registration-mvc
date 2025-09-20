# controllers/auth_controller.py
from models.database_manager import DatabaseManager
from typing import Optional, Tuple

class AuthController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Authenticate user
        Returns: (success, user_id, user_type)
        """
        if not username or not password:
            return False, None, None
        
        # Check if it's admin login
        if self.db_manager.authenticate_admin(username, password):
            return True, username, "admin"
        
        # Check if it's student login (using student_id as username)
        if self.db_manager.authenticate_student(username, password):
            return True, username, "student"
        
        return False, None, None
    
    def validate_student_age(self, student_id: str) -> bool:
        """Check if student is at least 15 years old"""
        from datetime import datetime, date
        
        student = self.db_manager.get_student_by_id(student_id)
        if not student:
            return False
        
        birth_date = datetime.strptime(student['birth_date'], '%Y-%m-%d').date()
        age = (date.today() - birth_date).days // 365
        return age >= 15
