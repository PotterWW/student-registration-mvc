# models/database_manager.py
import sqlite3
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path="student_registration.db"):
        self.db_path = db_path
        self.connection = None
    
    def get_connection(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                student_id TEXT PRIMARY KEY,
                prefix TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                birth_date DATE NOT NULL,
                current_school TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                program_code TEXT NOT NULL,
                password TEXT DEFAULT 'password123'
            )
        ''')
        
        # Programs table (for curriculum structure)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Programs (
                program_code TEXT PRIMARY KEY,
                program_name TEXT NOT NULL,
                department TEXT NOT NULL
            )
        ''')
        
        # Subjects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Subjects (
                subject_code TEXT PRIMARY KEY,
                subject_name TEXT NOT NULL,
                credits INTEGER CHECK(credits > 0),
                instructor TEXT NOT NULL,
                prerequisite TEXT DEFAULT NULL,
                FOREIGN KEY (prerequisite) REFERENCES Subjects(subject_code)
            )
        ''')
        
        # SubjectStructure table (curriculum requirements)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SubjectStructure (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_code TEXT NOT NULL,
                subject_code TEXT NOT NULL,
                semester INTEGER CHECK(semester IN (1, 2)),
                FOREIGN KEY (program_code) REFERENCES Programs(program_code),
                FOREIGN KEY (subject_code) REFERENCES Subjects(subject_code),
                UNIQUE(program_code, subject_code, semester)
            )
        ''')
        
        # RegisteredSubject table (student registrations and grades)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS RegisteredSubject (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                subject_code TEXT NOT NULL,
                grade TEXT CHECK(grade IN ('A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F', 'IP')) DEFAULT 'IP',
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES Students(student_id),
                FOREIGN KEY (subject_code) REFERENCES Subjects(subject_code),
                UNIQUE(student_id, subject_code)
            )
        ''')
        
        # Admin table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Admin (
                admin_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        conn.commit()
    
    def insert_sample_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM Students")
        if cursor.fetchone()[0] > 0:
            return
        
        # Insert Programs
        programs = [
            ('12345678', 'วิทยาการคอมพิวเตอร์', 'ภาควิชาวิทยาการคอมพิวเตอร์'),
            ('12345679', 'วิศวกรรมซอฟต์แวร์', 'ภาควิชาวิทยาการคอมพิวเตอร์'),
            ('12345680', 'คณิตศาสตร์ประยุกต์', 'ภาควิชาคณิตศาสตร์')
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO Programs (program_code, program_name, department) VALUES (?, ?, ?)",
            programs
        )
        
        # Insert Subjects
        subjects = [
            ('05500101', 'Computer Programming I', 3, 'อ.สมชาย', None),
            ('05500102', 'Computer Programming II', 3, 'อ.สมหญิง', '05500101'),
            ('05500201', 'Data Structures', 3, 'อ.วิชัย', '05500102'),
            ('05500301', 'Database Systems', 3, 'อ.มาลี', '05500201'),
            ('05500401', 'Software Engineering', 3, 'อ.ประยูร', '05500301'),
            ('90690101', 'English I', 3, 'อ.จอห์น', None),
            ('90690102', 'English II', 3, 'อ.เมรี่', '90690101'),
            ('90690201', 'Mathematics I', 3, 'อ.สุทธิพงษ์', None),
            ('90690202', 'Mathematics II', 3, 'อ.กมลพร', '90690201'),
            ('05500105', 'Web Development', 3, 'อ.นันทา', '05500102'),
            ('05500205', 'Algorithms', 3, 'อ.สมศักดิ์', '05500201')
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO Subjects (subject_code, subject_name, credits, instructor, prerequisite) VALUES (?, ?, ?, ?, ?)",
            subjects
        )
        
        # Insert SubjectStructure
        structure = [
            ('12345678', '05500101', 1),
            ('12345678', '90690101', 1),
            ('12345678', '90690201', 1),
            ('12345678', '05500102', 2),
            ('12345678', '90690102', 2),
            ('12345678', '90690202', 2),
            ('12345678', '05500201', 2),
            ('12345679', '05500101', 1),
            ('12345679', '90690101', 1),
            ('12345679', '05500105', 1),
            ('12345679', '05500102', 2),
            ('12345679', '05500201', 2)
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO SubjectStructure (program_code, subject_code, semester) VALUES (?, ?, ?)",
            structure
        )
        
        # Insert Students
        students = [
            ('69000001', 'นาย', 'สมชาย', 'ใจดี', '2007-01-15', 'โรงเรียนสมชาย', 'somchai@email.com', '12345678'),
            ('69000002', 'นางสาว', 'สมหญิง', 'รักเรียน', '2007-03-20', 'โรงเรียนดาวเด่น', 'somying@email.com', '12345678'),
            ('69000003', 'นาย', 'วิชัย', 'เก่งมาก', '2007-02-10', 'โรงเรียนวิทยา', 'wichai@email.com', '12345679'),
            ('69000004', 'นางสาว', 'มาลี', 'สวยงาม', '2006-12-05', 'โรงเรียนสายรุ้ง', 'malee@email.com', '12345678'),
            ('69000005', 'นาย', 'ประยูร', 'ฉลาด', '2007-04-25', 'โรงเรียนปัญญา', 'prayoon@email.com', '12345679'),
            ('69000006', 'นางสาว', 'กมลพร', 'เรียบร้อย', '2007-01-30', 'โรงเรียนคุณธรรม', 'kamolporn@email.com', '12345680'),
            ('69000007', 'นาย', 'นันทา', 'ซื่อสัตย์', '2006-11-12', 'โรงเรียนสุจริต', 'nanta@email.com', '12345678'),
            ('69000008', 'นางสาว', 'สุนิสา', 'มั่นใจ', '2007-05-08', 'โรงเรียนมั่นคง', 'sunisa@email.com', '12345679'),
            ('69000009', 'นาย', 'อภิชาต', 'กล้าหาญ', '2006-09-18', 'โรงเรียนหาดใหญ่', 'aphichat@email.com', '12345678'),
            ('69000010', 'นางสาว', 'วรรณา', 'อ่อนโยน', '2007-07-03', 'โรงเรียนสงขลา', 'wanna@email.com', '12345679'),
            ('69000011', 'นาย', 'ธนากร', 'มุ่งมั่น', '2006-10-22', 'โรงเรียนปัตตานี', 'thanakorn@email.com', '12345680')
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO Students (student_id, prefix, first_name, last_name, birth_date, current_school, email, program_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            students
        )
        
        # Insert some grades for testing prerequisites
        registered_subjects = [
            ('69000001', '05500101', 'B+'),
            ('69000001', '90690101', 'A'),
            ('69000001', '90690201', 'B'),
            ('69000002', '05500101', 'A'),
            ('69000002', '90690101', 'B+'),
            ('69000003', '05500101', 'C+'),
            ('69000004', '90690101', 'A')
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO RegisteredSubject (student_id, subject_code, grade) VALUES (?, ?, ?)",
            registered_subjects
        )
        
        # Insert Admin
        cursor.execute(
            "INSERT OR IGNORE INTO Admin (admin_id, username, password) VALUES (?, ?, ?)",
            ('admin001', 'admin', 'admin123')
        )
        
        conn.commit()
    
    # Student-related methods
    def get_student_by_id(self, student_id: str) -> Optional[Dict]:
        cursor = self.get_connection().cursor()
        cursor.execute("""
            SELECT s.*, p.program_name, p.department
            FROM Students s
            JOIN Programs p ON s.program_code = p.program_code
            WHERE s.student_id = ?
        """, (student_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_students(self) -> List[Dict]:
        cursor = self.get_connection().cursor()
        cursor.execute("""
            SELECT s.*, p.program_name, p.department
            FROM Students s
            JOIN Programs p ON s.program_code = p.program_code
            ORDER BY s.first_name, s.last_name
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def authenticate_student(self, student_id: str, password: str) -> bool:
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT password FROM Students WHERE student_id = ?", (student_id,))
        row = cursor.fetchone()
        return row and row['password'] == password
    
    def authenticate_admin(self, username: str, password: str) -> bool:
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT password FROM Admin WHERE username = ?", (username,))
        row = cursor.fetchone()
        return row and row['password'] == password
    
    # Subject-related methods
    def get_available_subjects_for_student(self, student_id: str) -> List[Dict]:
        cursor = self.get_connection().cursor()
        cursor.execute("""
            SELECT DISTINCT s.*, ss.semester
            FROM Subjects s
            JOIN SubjectStructure ss ON s.subject_code = ss.subject_code
            JOIN Students st ON ss.program_code = st.program_code
            WHERE st.student_id = ?
            AND s.subject_code NOT IN (
                SELECT subject_code FROM RegisteredSubject WHERE student_id = ?
            )
            ORDER BY ss.semester, s.subject_code
        """, (student_id, student_id))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_student_registered_subjects(self, student_id: str) -> List[Dict]:
        cursor = self.get_connection().cursor()
        cursor.execute("""
            SELECT s.*, rs.grade, rs.registration_date
            FROM Subjects s
            JOIN RegisteredSubject rs ON s.subject_code = rs.subject_code
            WHERE rs.student_id = ?
            ORDER BY rs.registration_date
        """, (student_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def check_prerequisite(self, student_id: str, subject_code: str) -> Tuple[bool, str]:
        cursor = self.get_connection().cursor()
        
        # Get prerequisite
        cursor.execute("SELECT prerequisite FROM Subjects WHERE subject_code = ?", (subject_code,))
        row = cursor.fetchone()
        
        if not row or not row['prerequisite']:
            return True, "ไม่มีวิชาบังคับก่อน"
        
        prerequisite = row['prerequisite']
        
        # Check if student passed prerequisite
        cursor.execute("""
            SELECT grade FROM RegisteredSubject 
            WHERE student_id = ? AND subject_code = ?
        """, (student_id, prerequisite))
        
        grade_row = cursor.fetchone()
        if not grade_row:
            return False, f"ต้องเรียนวิชา {prerequisite} ก่อน"
        
        grade = grade_row['grade']
        if grade in ['F', 'IP']:
            return False, f"ต้องสอบผ่านวิชา {prerequisite} ก่อน (เกรดปัจจุบัน: {grade})"
        
        return True, "เรียนครบวิชาบังคับก่อนแล้ว"
    
    def register_subject(self, student_id: str, subject_code: str) -> Tuple[bool, str]:
        # Check age
        student = self.get_student_by_id(student_id)
        if not student:
            return False, "ไม่พบข้อมูลนักเรียน"
        
        birth_date = datetime.strptime(student['birth_date'], '%Y-%m-%d').date()
        age = (date.today() - birth_date).days // 365
        if age < 15:
            return False, "นักเรียนต้องมีอายุอย่างน้อย 15 ปี"
        
        # Check prerequisite
        can_register, message = self.check_prerequisite(student_id, subject_code)
        if not can_register:
            return False, message
        
        # Register subject
        try:
            cursor = self.get_connection().cursor()
            cursor.execute("""
                INSERT INTO RegisteredSubject (student_id, subject_code)
                VALUES (?, ?)
            """, (student_id, subject_code))
            self.get_connection().commit()
            return True, "ลงทะเบียนสำเร็จ"
        except sqlite3.IntegrityError:
            return False, "ลงทะเบียนวิชานี้แล้ว"
    
    def get_subject_registrations(self, subject_code: str) -> List[Dict]:
        cursor = self.get_connection().cursor()
        cursor.execute("""
            SELECT s.*, rs.grade, rs.registration_date
            FROM Students s
            JOIN RegisteredSubject rs ON s.student_id = rs.student_id
            WHERE rs.subject_code = ?
            ORDER BY s.first_name, s.last_name
        """, (subject_code,))
        return [dict(row) for row in cursor.fetchall()]
    
    def update_grade(self, student_id: str, subject_code: str, grade: str) -> bool:
        try:
            cursor = self.get_connection().cursor()
            cursor.execute("""
                UPDATE RegisteredSubject 
                SET grade = ?
                WHERE student_id = ? AND subject_code = ?
            """, (grade, student_id, subject_code))
            self.get_connection().commit()
            return True
        except:
            return False
    
    def get_all_subjects(self) -> List[Dict]:
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM Subjects ORDER BY subject_code")
        return [dict(row) for row in cursor.fetchall()]
    
    def search_students(self, search_term: str = "", school_filter: str = "", sort_by: str = "name") -> List[Dict]:
        cursor = self.get_connection().cursor()
        
        query = """
            SELECT s.*, p.program_name, p.department
            FROM Students s
            JOIN Programs p ON s.program_code = p.program_code
            WHERE 1=1
        """
        params = []
        
        if search_term:
            query += " AND (s.first_name LIKE ? OR s.last_name LIKE ? OR s.student_id LIKE ?)"
            search_param = f"%{search_term}%"
            params.extend([search_param, search_param, search_param])
        
        if school_filter:
            query += " AND s.current_school LIKE ?"
            params.append(f"%{school_filter}%")
        
        if sort_by == "name":
            query += " ORDER BY s.first_name, s.last_name"
        elif sort_by == "age":
            query += " ORDER BY s.birth_date DESC"
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_schools(self) -> List[str]:
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT DISTINCT current_school FROM Students ORDER BY current_school")
        return [row[0] for row in cursor.fetchall()]
