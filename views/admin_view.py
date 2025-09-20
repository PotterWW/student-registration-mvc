# views/admin_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List

class AdminView:
    def __init__(self, parent, admin_controller, logout_callback):
        self.parent = parent
        self.admin_controller = admin_controller
        self.logout_callback = logout_callback
        self.selected_student_id = None
        
        # Clear the parent window
        for widget in parent.winfo_children():
            widget.destroy()
        
        self.setup_ui()
        self.load_students_data()
    
    def setup_ui(self):
        # Main frame with notebook (tabs)
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Students management tab
        self.students_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.students_frame, text="จัดการนักเรียน")
        
        # Grade entry tab
        self.grades_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.grades_frame, text="กรอกเกรด")
        
        # Setup tabs
        self.setup_students_tab()
        self.setup_grades_tab()
        
        # Logout button
        logout_frame = ttk.Frame(self.parent)
        logout_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(logout_frame, text="ออกจากระบบ", 
                  command=self.logout_callback).pack(side='right')
    
    def setup_students_tab(self):
        # Search and filter frame
        search_frame = ttk.LabelFrame(self.students_frame, text="ค้นหาและกรอง", padding=10)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        # Search entry
        ttk.Label(search_frame, text="ค้นหา:").grid(row=0, column=0, sticky='w', padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, sticky='ew', padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # School filter
        ttk.Label(search_frame, text="โรงเรียน:").grid(row=0, column=2, sticky='w', padx=5)
        self.school_var = tk.StringVar()
        self.school_combo = ttk.Combobox(search_frame, textvariable=self.school_var, state='readonly')
        self.school_combo.grid(row=0, column=3, sticky='ew', padx=5)
        self.school_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Sort option
        ttk.Label(search_frame, text="เรียงตาม:").grid(row=0, column=4, sticky='w', padx=5)
        self.sort_var = tk.StringVar(value="name")
        sort_combo = ttk.Combobox(search_frame, textvariable=self.sort_var, 
                                values=["name", "age"], state='readonly')
        sort_combo.grid(row=0, column=5, sticky='ew', padx=5)
        sort_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Configure grid weights
        search_frame.columnconfigure(1, weight=1)
        search_frame.columnconfigure(3, weight=1)
        
        # Students list frame
        list_frame = ttk.LabelFrame(self.students_frame, text="รายชื่อนักเรียน", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for students
        columns = ('รหัสนักเรียน', 'ชื่อ', 'นามสกุล', 'อายุ', 'โรงเรียน', 'หลักสูตร')
        self.students_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            if col in ['ชื่อ', 'นามสกุล']:
                self.students_tree.column(col, width=120)
            elif col == 'โรงเรียน':
                self.students_tree.column(col, width=150)
            elif col == 'หลักสูตร':
                self.students_tree.column(col, width=200)
            else:
                self.students_tree.column(col, width=100)
        
        # Scrollbar for students
        students_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', 
                                         command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=students_scrollbar.set)
        
        self.students_tree.pack(side='left', fill='both', expand=True)
        students_scrollbar.pack(side='right', fill='y')
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.students_frame)
        buttons_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(buttons_frame, text="ดูประวัตินักเรียน", 
                  command=self.view_student_profile).pack(side='left', padx=5)
        
        ttk.Button(buttons_frame, text="รีเฟรช", 
                  command=self.refresh_students).pack(side='left', padx=5)
        
        # Bind double-click to view profile
        self.students_tree.bind('<Double-1>', lambda e: self.view_student_profile())
    
    def setup_grades_tab(self):
        # Subject selection frame
        subject_frame = ttk.LabelFrame(self.grades_frame, text="เลือกรายวิชา", padding=10)
        subject_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(subject_frame, text="รายวิชา:").pack(side='left')
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(subject_frame, textvariable=self.subject_var, 
                                        state='readonly', width=50)
        self.subject_combo.pack(side='left', padx=10, fill='x', expand=True)
        self.subject_combo.bind('<<ComboboxSelected>>', self.on_subject_selected)
        
        ttk.Button(subject_frame, text="โหลดรายชื่อ", 
                  command=self.load_subject_registrations).pack(side='right', padx=5)
        
        # Registrations frame
        reg_frame = ttk.LabelFrame(self.grades_frame, text="นักเรียนที่ลงทะเบียน", padding=10)
        reg_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for registrations
        columns = ('รหัสนักเรียน', 'ชื่อ-นามสกุล', 'โรงเรียน', 'เกรดปัจจุบัน', 'วันที่ลงทะเบียน')
        self.registrations_tree = ttk.Treeview(reg_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.registrations_tree.heading(col, text=col)
            if col == 'ชื่อ-นามสกุล':
                self.registrations_tree.column(col, width=200)
            elif col == 'โรงเรียน':
                self.registrations_tree.column(col, width=150)
            else:
                self.registrations_tree.column(col, width=120)
        
        # Scrollbar for registrations
        reg_scrollbar = ttk.Scrollbar(reg_frame, orient='vertical', 
                                    command=self.registrations_tree.yview)
        self.registrations_tree.configure(yscrollcommand=reg_scrollbar.set)
        
        self.registrations_tree.pack(side='left', fill='both', expand=True)
        reg_scrollbar.pack(side='right', fill='y')
        
        # Grade entry frame
        grade_frame = ttk.Frame(self.grades_frame)
        grade_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(grade_frame, text="เกรด:").pack(side='left')
        self.grade_var = tk.StringVar()
        grade_combo = ttk.Combobox(grade_frame, textvariable=self.grade_var,
                                 values=['A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F', 'IP'],
                                 state='readonly', width=10)
        grade_combo.pack(side='left', padx=10)
        
        ttk.Button(grade_frame, text="อัพเดทเกรด", 
                  command=self.update_selected_grade).pack(side='left', padx=5)
        
        # Statistics label
        self.stats_label = ttk.Label(self.grades_frame, text="", foreground='blue')
        self.stats_label.pack(pady=5)
    
    def load_students_data(self):
        # Load schools for filter
        schools = ['ทั้งหมด'] + self.admin_controller.get_schools()
        self.school_combo['values'] = schools
        self.school_combo.set('ทั้งหมด')
        
        # Load subjects for grade entry
        subjects = self.admin_controller.get_all_subjects()
        subject_options = [f"{s['subject_code']}: {s['subject_name']}" for s in subjects]
        self.subject_combo['values'] = subject_options
        
        # Load students
        self.refresh_students()
    
    def refresh_students(self):
        # Clear existing items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Get filter values
        search_term = self.search_entry.get()
        school_filter = self.school_var.get() if self.school_var.get() != 'ทั้งหมด' else ''
        sort_by = self.sort_var.get()
        
        # Load students with filters
        students = self.admin_controller.search_students(search_term, school_filter, sort_by)
        
        for student in students:
            # Calculate age
            from datetime import datetime, date
            birth_date = datetime.strptime(student['birth_date'], '%Y-%m-%d').date()
            age = (date.today() - birth_date).days // 365
            
            values = (
                student['student_id'],
                student['first_name'],
                student['last_name'],
                f"{age} ปี",
                student['current_school'],
                student['program_name']
            )
            self.students_tree.insert('', 'end', values=values)
    
    def on_search_change(self, event):
        self.refresh_students()
    
    def on_filter_change(self, event):
        self.refresh_students()
    
    def view_student_profile(self):
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกนักเรียนที่ต้องการดูประวัติ")
            return
        
        item = selection[0]
        student_id = self.students_tree.item(item)['values'][0]
        
        # Open student profile window
        self.open_student_profile_window(student_id)
    
    def open_student_profile_window(self, student_id):
        # Create new window for student profile
        profile_window = tk.Toplevel(self.parent)
        profile_window.title(f"ประวัตินักเรียน - {student_id}")
        profile_window.geometry("800x600")
        
        # Get student data
        student = self.admin_controller.get_student_details(student_id)
        registered_subjects = self.admin_controller.get_student_registered_subjects(student_id)
        
        if not student:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบข้อมูลนักเรียน")
            profile_window.destroy()
            return
        
        # Student info frame
        info_frame = ttk.LabelFrame(profile_window, text="ข้อมูลส่วนตัว", padding=10)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        # Calculate age
        from datetime import datetime, date
        birth_date = datetime.strptime(student['birth_date'], '%Y-%m-%d').date()
        age = (date.today() - birth_date).days // 365
        
        info_data = [
            ("รหัสนักเรียน:", student['student_id']),
            ("ชื่อ-นามสกุล:", f"{student['prefix']}{student['first_name']} {student['last_name']}"),
            ("วันเกิด:", f"{student['birth_date']} (อายุ {age} ปี)"),
            ("โรงเรียนปัจจุบัน:", student['current_school']),
            ("อีเมล:", student['email']),
            ("หลักสูตร:", f"{student['program_name']} ({student['department']})")
        ]
        
        for i, (label, value) in enumerate(info_data):
            ttk.Label(info_frame, text=label).grid(row=i, column=0, sticky='w', pady=3)
            ttk.Label(info_frame, text=value, foreground='blue').grid(row=i, column=1, sticky='w', padx=(20, 0), pady=3)
        
        # Registered subjects frame
        subjects_frame = ttk.LabelFrame(profile_window, text="รายวิชาที่ลงทะเบียนแล้ว", padding=10)
        subjects_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for subjects
        columns = ('รหัสวิชา', 'ชื่อวิชา', 'หน่วยกิต', 'เกรด', 'วันที่ลงทะเบียน')
        subjects_tree = ttk.Treeview(subjects_frame, columns=columns, show='headings')
        
        for col in columns:
            subjects_tree.heading(col, text=col)
            subjects_tree.column(col, width=120 if col != 'ชื่อวิชา' else 200)
        
        for subject in registered_subjects:
            reg_date = subject['registration_date'].split()[0]  # Get date part only
            values = (
                subject['subject_code'],
                subject['subject_name'],
                subject['credits'],
                subject['grade'],
                reg_date
            )
            subjects_tree.insert('', 'end', values=values)
        
        # Scrollbar
        subjects_scrollbar = ttk.Scrollbar(subjects_frame, orient='vertical', 
                                         command=subjects_tree.yview)
        subjects_tree.configure(yscrollcommand=subjects_scrollbar.set)
        
        subjects_tree.pack(side='left', fill='both', expand=True)
        subjects_scrollbar.pack(side='right', fill='y')
        
        # Statistics
        total_subjects = len(registered_subjects)
        completed_credits = sum(s['credits'] for s in registered_subjects if s['grade'] not in ['F', 'IP'])
        
        stats_text = f"รวม: {total_subjects} วิชา | หน่วยกิตที่ผ่าน: {completed_credits} หน่วยกิต"
        ttk.Label(profile_window, text=stats_text, foreground='green').pack(pady=5)
    
    def on_subject_selected(self, event):
        self.load_subject_registrations()
    
    def load_subject_registrations(self):
        selected_subject = self.subject_var.get()
        if not selected_subject:
            return
        
        # Extract subject code
        subject_code = selected_subject.split(':')[0]
        
        # Clear existing items
        for item in self.registrations_tree.get_children():
            self.registrations_tree.delete(item)
        
        # Load registrations
        registrations = self.admin_controller.get_subject_registrations(subject_code)
        
        for reg in registrations:
            reg_date = reg['registration_date'].split()[0]  # Get date part only
            values = (
                reg['student_id'],
                f"{reg['prefix']}{reg['first_name']} {reg['last_name']}",
                reg['current_school'],
                reg['grade'],
                reg_date
            )
            self.registrations_tree.insert('', 'end', values=values)
        
        # Update statistics
        total_count = len(registrations)
        grade_counts = {}
        for reg in registrations:
            grade = reg['grade']
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
        
        stats_text = f"จำนวนนักเรียนที่ลงทะเบียน: {total_count} คน"
        if grade_counts:
            grade_stats = " | ".join([f"{grade}: {count}" for grade, count in grade_counts.items()])
            stats_text += f" | เกรด: {grade_stats}"
        
        self.stats_label.config(text=stats_text)
    
    def update_selected_grade(self):
        # Check if subject is selected
        if not self.subject_var.get():
            messagebox.showwarning("คำเตือน", "กรุณาเลือกรายวิชาก่อน")
            return
        
        # Check if student is selected
        selection = self.registrations_tree.selection()
        if not selection:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกนักเรียนที่ต้องการอัพเดทเกรด")
            return
        
        # Check if grade is selected
        new_grade = self.grade_var.get()
        if not new_grade:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกเกรดที่ต้องการให้")
            return
        
        # Get selected data
        item = selection[0]
        student_id = self.registrations_tree.item(item)['values'][0]
        student_name = self.registrations_tree.item(item)['values'][1]
        subject_code = self.subject_var.get().split(':')[0]
        
        # Confirm update
        result = messagebox.askyesno("ยืนยันการอัพเดท", 
                                   f"ต้องการอัพเดทเกรดของ\n{student_name} ({student_id})\n"
                                   f"เป็น {new_grade} ใช่หรือไม่?")
        
        if result:
            success = self.admin_controller.update_student_grade(student_id, subject_code, new_grade)
            
            if success:
                messagebox.showinfo("สำเร็จ", "อัพเดทเกรดเรียบร้อยแล้ว")
                self.load_subject_registrations()  # Refresh the list
                self.grade_var.set('')  # Clear grade selection
            else:
                messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถอัพเดทเกรดได้")
    
    def destroy(self):
        # Clear the parent window
        for widget in self.parent.winfo_children():
            widget.destroy()
