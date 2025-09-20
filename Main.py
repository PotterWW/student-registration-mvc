# main.py
import tkinter as tk
from tkinter import ttk
from controllers.auth_controller import AuthController
from controllers.student_controller import StudentController
from controllers.admin_controller import AdminController
from models.database_manager import DatabaseManager
from views.login_view import LoginView

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ระบบลงทะเบียนเรียนล่วงหน้า")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize database
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()
        self.db_manager.insert_sample_data()
        
        # Initialize controllers
        self.auth_controller = AuthController(self.db_manager)
        self.student_controller = StudentController(self.db_manager)
        self.admin_controller = AdminController(self.db_manager)
        
        # Initialize current view
        self.current_view = None
        self.current_user = None
        
        # Show login screen
        self.show_login()
    
    def show_login(self):
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = LoginView(self.root, self.on_login_success)
    
    def on_login_success(self, user_id, user_type):
        self.current_user = {"id": user_id, "type": user_type}
        
        if user_type == "admin":
            self.show_admin_dashboard()
        else:
            self.show_student_dashboard()
    
    def show_admin_dashboard(self):
        if self.current_view:
            self.current_view.destroy()
        
        from views.admin_view import AdminView
        self.current_view = AdminView(
            self.root, 
            self.admin_controller,
            self.logout
        )
    
    def show_student_dashboard(self):
        if self.current_view:
            self.current_view.destroy()
        
        from views.student_view import StudentView
        self.current_view = StudentView(
            self.root,
            self.student_controller,
            self.current_user["id"],
            self.logout
        )
    
    def logout(self):
        self.current_user = None
        self.show_login()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run()