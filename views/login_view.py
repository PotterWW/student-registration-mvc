# views/login_view.py
import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    def __init__(self, parent, on_login_callback):
        self.parent = parent
        self.on_login_callback = on_login_callback
        
        # Clear the parent window
        for widget in parent.winfo_children():
            widget.destroy()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Title
        title_label = ttk.Label(main_frame, text="ระบบลงทะเบียนเรียนล่วงหน้า", 
                               font=('TH SarabunPSK', 24, 'bold'))
        title_label.pack(pady=20)
        
        # Login frame
        login_frame = ttk.LabelFrame(main_frame, text="เข้าสู่ระบบ", padding=20)
        login_frame.pack(pady=20, padx=50, fill='x')
        
        # Username
        ttk.Label(login_frame, text="รหัสผู้ใช้:").grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = ttk.Entry(login_frame, font=('TH SarabunPSK', 12))
        self.username_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(login_frame, text="รหัสผ่าน:").grid(row=1, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*", font=('TH SarabunPSK', 12))
        self.password_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Login button
        login_btn = ttk.Button(login_frame, text="เข้าสู่ระบบ", command=self.handle_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Configure column weight
        login_frame.columnconfigure(1, weight=1)
        
        # Bind Enter key
        self.parent.bind('<Return>', lambda e: self.handle_login())
        
        # Instructions
        instructions = ttk.Label(main_frame, 
                               text="สำหรับนักเรียน: ใช้รหัสนักเรียน 8 หลัก (เช่น 69000001) รหัสผ่าน: password123\n"
                                    "สำหรับแอดมิน: ใช้ username: admin รหัสผ่าน: admin123",
                               font=('TH SarabunPSK', 10),
                               foreground='gray')
        instructions.pack(pady=10)
        
        # Set focus to username entry
        self.username_entry.focus()
    
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกรหัสผู้ใช้และรหัสผ่าน")
            return
        
        # Import here to avoid circular imports
        from controllers.auth_controller import AuthController
        from models.database_manager import DatabaseManager
        
        db_manager = DatabaseManager()
        auth_controller = AuthController(db_manager)
        
        success, user_id, user_type = auth_controller.authenticate(username, password)
        
        if success:
            self.on_login_callback(user_id, user_type)
        else:
            messagebox.showerror("ข้อผิดพลาด", "รหัสผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
            self.password_entry.delete(0, tk.END)
    
    def destroy(self):
        # Clear the parent window
        for widget in self.parent.winfo_children():
            widget.destroy()
