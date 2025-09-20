# views/student_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List

class StudentView:
    def __init__(self, parent, student_controller, student_id, logout_callback):
        self.parent = parent
        self.student_controller = student_controller
        self.student_id = student_id
        self.logout_callback = logout_callback
        
        # Clear the parent window
        for widget in parent.winfo_children():
            widget.destroy()
        
        self.setup_ui()
        self.load_student_data()
    
    def setup_ui(self):
        # Main frame with notebook (tabs)
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Profile tab
        self.profile_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.profile_frame, text="ประวัตินักเรียน")
        
        # Registration tab
        self.registration_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.registration_frame, text="ลงทะเบียนเรียน")
        
        # Setup profile tab
        self.setup_profile_tab()
        
        # Setup registration tab
        self.setup_registration_tab()
        
        # Logout button
        logout_frame = ttk.Frame(self.parent)
        logout_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(logout_frame, text="ออกจากระบบ", 
                  command=self.logout_callback).pack(side='right')
    
    def setup_profile_tab(self):
        # Student info frame
        info_frame = ttk.LabelFrame(self.profile_frame, text="ข้อมูลส่วนตัว", padding=10)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        self.info_labels = {}
        info_fields = [
            ("รหัสนักเรียน:", "student_id"),
            ("ชื่อ-นามสกุล:", "full_name"),
            ("วันเกิด:", "birth_date"),
            ("อายุ:", "age"),
            ("โรงเรียนปัจจุบัน:", "current_school"),
            ("อีเมล:", "email"),
            ("หลักสูตร:", "program_info"),
            ("GPA:", "gpa"),
            ("หน่วยกิตที่ผ่าน:", "completed_credits")
        ]
        
        for i, (label_text, key) in enumerate(info_fields):
            ttk.Label(info_frame, text=label_text).grid(row=i, column=0, sticky='w', pady=3)
            label = ttk.Label(info_frame, text="", foreground='blue')
            label.grid(row=i, column=1, sticky='w', padx=(20, 0), pady=3)
            self.info_labels[key] = label
        
        # Registered subjects frame
        subjects_frame = ttk.LabelFrame(self.profile_frame, text="รายวิชาที่ลงทะเบียนแล้ว", padding=10)
        subjects_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for registered subjects
        columns = ('รหัสวิชา', 'ชื่อวิชา', 'หน่วยกิต', 'อาจารย์', 'เกรด', 'วันที่ลงทะเบียน')
        self.registered_tree = ttk.Treeview(subjects_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.registered_tree.heading(col, text=col)
            self.registered_tree.column(col, width=120)
        
        # Scrollbar for registered subjects
        registered_scrollbar = ttk.Scrollbar(subjects_frame, orient='vertical', 
                                           command=self.registered_tree.yview)
        self.registered_tree.configure(yscrollcommand=registered_scrollbar.set)
        
        self.registered_tree.pack(side='left', fill='both', expand=True)
        registered_scrollbar.pack(side='right', fill='y')
    
    def setup_registration_tab(self):
        # Available subjects frame
        available_frame = ttk.LabelFrame(self.registration_frame, text="รายวิชาที่สามารถลงทะเบียนได้", padding=10)
        available_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for available subjects
        columns = ('รหัสวิชา', 'ชื่อวิชา', 'หน่วยกิต', 'อาจารย์', 'เทอม', 'สถานะ', 'หมายเหตุ')
        self.available_tree = ttk.Treeview(available_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.available_tree.heading(col, text=col)
            if col == 'ชื่อวิชา':
                self.available_tree.column(col, width=200)
            elif col == 'หมายเหตุ':
                self.available_tree.column(col, width=150)
            else:
                self.available_tree.column(col, width=100)
        
        # Scrollbar for available subjects
        available_scrollbar = ttk.Scrollbar(available_frame, orient='vertical', 
                                          command=self.available_tree.yview)
        self.available_tree.configure(yscrollcommand=available_scrollbar.set)
        
        self.available_tree.pack(side='left', fill='both', expand=True)
        available_scrollbar.pack(side='right', fill='y')
        
        # Register button
        button_frame = ttk.Frame(self.registration_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="ลงทะเบียนวิชาที่เลือก", 
                  command=self.register_selected_subject).pack()
        
        ttk.Button(button_frame, text="รีเฟรชข้อมูล", 
                  command=self.refresh_available_subjects).pack(pady=5)
        
        # Bind double-click to register
        self.available_tree.bind('<Double-1>', lambda e: self.register_selected_subject())
    
    def load_student_data(self):
        # Load student profile
        profile = self.student_controller.get_student_profile(self.student_id)
        if profile:
            # Calculate age
            from datetime import datetime, date
            birth_date = datetime.strptime(profile['birth_date'], '%Y-%m-%d').date()
            age = (date.today() - birth_date).days // 365
            
            # Update info labels
            self.info_labels['student_id'].config(text=profile['student_id'])
            self.info_labels['full_name'].config(text=f"{profile['prefix']}{profile['first_name']} {profile['last_name']}")
            self.info_labels['birth_date'].config(text=profile['birth_date'])
            self.info_labels['age'].config(text=f"{age} ปี")
            self.info_labels['current_school'].config(text=profile['current_school'])
            self.info_labels['email'].config(text=profile['email'])
            self.info_labels['program_info'].config(text=f"{profile['program_name']} ({profile['department']})")
            
            # Calculate and display GPA and credits
            gpa = self.student_controller.get_student_gpa(self.student_id)
            credits = self.student_controller.get_completed_credits(self.student_id)
            self.info_labels['gpa'].config(text=f"{gpa:.2f}")
            self.info_labels['completed_credits'].config(text=f"{credits} หน่วยกิต")
        
        # Load registered subjects
        self.load_registered_subjects()
        
        # Load available subjects
        self.load_available_subjects()
    
    def load_registered_subjects(self):
        # Clear existing items
        for item in self.registered_tree.get_children():
            self.registered_tree.delete(item)
        
        subjects = self.student_controller.get_student_registered_subjects(self.student_id)
        for subject in subjects:
            # Format registration date
            reg_date = subject['registration_date'].split()[0]  # Get date part only
            
            values = (
                subject['subject_code'],
                subject['subject_name'],
                subject['credits'],
                subject['instructor'],
                subject['grade'],
                reg_date
            )
            self.registered_tree.insert('', 'end', values=values)
    
    def load_available_subjects(self):
        # Clear existing items
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)
        
        subjects = self.student_controller.get_available_subjects(self.student_id)
        for subject in subjects:
            status = "✓ ลงได้" if subject['can_register'] else "✗ ลงไม่ได้"
            
            values = (
                subject['subject_code'],
                subject['subject_name'],
                subject['credits'],
                subject['instructor'],
                subject['semester'],
                status,
                subject['prerequisite_status']
            )
            
            item = self.available_tree.insert('', 'end', values=values)
            
            # Color code the items
            if not subject['can_register']:
                self.available_tree.set(item, '0', subject['subject_code'])
                # You might want to change the foreground color here
    
    def refresh_available_subjects(self):
        """Refresh the available subjects list"""
        self.load_available_subjects()
        messagebox.showinfo("สำเร็จ", "รีเฟรชข้อมูลเรียบร้อยแล้ว")
    
    def register_selected_subject(self):
        selection = self.available_tree.selection()
        if not selection:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกวิชาที่ต้องการลงทะเบียน")
            return
        
        item = selection[0]
        subject_code = self.available_tree.item(item)['values'][0]
        subject_name = self.available_tree.item(item)['values'][1]
        status = self.available_tree.item(item)['values'][5]
        
        if "ลงไม่ได้" in status:
            messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถลงทะเบียนวิชานี้ได้ กรุณาตรวจสอบข้อกำหนด")
            return
        
        # Confirm registration
        result = messagebox.askyesno("ยืนยันการลงทะเบียน", 
                                   f"คุณต้องการลงทะเบียนวิชา\n{subject_code}: {subject_name}\nใช่หรือไม่?")
        
        if result:
            success, message = self.student_controller.register_for_subject(self.student_id, subject_code)
            
            if success:
                messagebox.showinfo("สำเร็จ", message)
                # Switch to profile tab and refresh data
                self.notebook.select(0)  # Select profile tab
                self.load_student_data()
            else:
                messagebox.showerror("ข้อผิดพลาด", message)
    
    def destroy(self):
        # Clear the parent window
        for widget in self.parent.winfo_children():
            widget.destroy()
