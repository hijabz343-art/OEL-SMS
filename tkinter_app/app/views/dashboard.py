import tkinter as tk
from app.utils.style import *
from app.services.auth import auth_service
from .student_registration import StudentRegistrationView
from .teacher_management import TeacherManagementView
from .class_scheduling import ClassSchedulingView
from .attendance_tracking import AttendanceTrackingView
from .fee_management import FeeManagementView
from .reports_dashboard import ReportsDashboardView

class DashboardView(tk.Frame):
    def __init__(self, parent, on_logout):
        super().__init__(parent, bg=COLOR_WHITE)
        self.on_logout = on_logout
        self.current_view = None
        self.create_widgets()

    def create_widgets(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=COLOR_NAVY_BLUE, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Main Content Area
        self.main_content = tk.Frame(self, bg=COLOR_WHITE)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Welcome Text
        user = auth_service.get_current_user()
        welcome_lbl = tk.Label(self.sidebar, text=f"Welcome,\n{user.username}", bg=COLOR_NAVY_BLUE, fg=COLOR_WHITE, font=FONT_HEADING)
        welcome_lbl.pack(pady=20)

        # Navigation Buttons
        self.add_nav_button("Students", lambda: self.show_view(StudentRegistrationView))
        
        if user.role == 'Admin':
            self.add_nav_button("Teachers", lambda: self.show_view(TeacherManagementView))
        
        self.add_nav_button("Classes", lambda: self.show_view(ClassSchedulingView))
        self.add_nav_button("Attendance", lambda: self.show_view(AttendanceTrackingView))
        
        if user.role == 'Admin':
            self.add_nav_button("Fees", lambda: self.show_view(FeeManagementView))
        
        self.add_nav_button("Reports", lambda: self.show_view(ReportsDashboardView))

        # Logout
        logout_btn = tk.Button(self.sidebar, text="Logout", bg=COLOR_ORANGE, fg=COLOR_WHITE, font=FONT_BODY, command=self.handle_logout)
        logout_btn.pack(side=tk.BOTTOM, pady=20, fill=tk.X, padx=10)

        # Show initial view
        self.show_view(StudentRegistrationView)

    def add_nav_button(self, text, command):
        btn = tk.Button(self.sidebar, text=text, bg=COLOR_NAVY_BLUE, fg=COLOR_WHITE, font=FONT_BODY, command=command, relief=tk.FLAT, anchor="w", padx=20)
        btn.pack(fill=tk.X, pady=5)
        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_ORANGE))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_NAVY_BLUE))

    def show_view(self, view_class):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = view_class(self.main_content)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def handle_logout(self):
        auth_service.logout()
        self.on_logout()
