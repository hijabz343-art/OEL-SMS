import tkinter as tk
from tkinter import messagebox
from app.utils.style import *
from app.services.auth import auth_service

class LoginView(tk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent, bg=COLOR_WHITE)
        self.on_login_success = on_login_success
        self.create_widgets()

    def create_widgets(self):
        # Header
        header = create_header(self, "School Management System - Login")
        header.pack(fill=tk.X)

        # Container for login form
        form_frame = tk.Frame(self, bg=COLOR_WHITE, pady=50)
        form_frame.pack(expand=True)

        create_label(form_frame, "Username:", font=FONT_HEADING).grid(row=0, column=0, pady=10, sticky=tk.E)
        self.entry_username = create_entry(form_frame)
        self.entry_username.grid(row=0, column=1, pady=10, padx=10)

        create_label(form_frame, "Password:", font=FONT_HEADING).grid(row=1, column=0, pady=10, sticky=tk.E)
        self.entry_password = tk.Entry(form_frame, font=FONT_BODY, width=30, show="*")
        self.entry_password.grid(row=1, column=1, pady=10, padx=10)

        login_btn = create_button(form_frame, "Login", self.handle_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=30)

    def handle_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        user = auth_service.login(username, password)
        if user:
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
