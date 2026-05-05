import sys
import os

# Add the parent directory to sys.path to allow 'app.' imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from app.utils.style import create_main_window
from app.views.login import LoginView
from app.views.dashboard import DashboardView
from app.services.db_service import db

class SchoolManagementApp:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        
        # Check DB connection on startup
        if not db.connect():
            # Connection failed, show empty window with error handled by db_service
            return
            
        self.show_login()

    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = LoginView(self.root, self.on_login_success)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def on_login_success(self, user):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = DashboardView(self.root, self.show_login)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = create_main_window()
    app = SchoolManagementApp(root)
    root.mainloop()

