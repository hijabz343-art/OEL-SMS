import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from app.utils.style import *
from app.services.db_service import db

class AttendanceTrackingView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_WHITE)
        self.student_map = {}
        self.create_widgets()
        self.load_students()
        self.load_data()

    def create_widgets(self):
        create_header(self, "Attendance Tracking").pack(fill=tk.X)

        form_frame = tk.Frame(self, bg=COLOR_WHITE, pady=10)
        form_frame.pack(fill=tk.X, padx=20)

        self.var_id = tk.StringVar()
        self.var_student = tk.StringVar()
        self.var_date = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        self.var_status = tk.StringVar()

        create_label(form_frame, "Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(form_frame, textvariable=self.var_date, font=FONT_BODY, width=20).grid(row=0, column=1, padx=5, pady=5)

        create_label(form_frame, "Student:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.combo_student = ttk.Combobox(form_frame, textvariable=self.var_student, font=FONT_BODY, width=25, state="readonly")
        self.combo_student.grid(row=0, column=3, padx=5, pady=5)

        create_label(form_frame, "Status:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_status = ttk.Combobox(form_frame, textvariable=self.var_status, font=FONT_BODY, width=18, state="readonly")
        self.combo_status['values'] = ("Present", "Absent")
        self.combo_status.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self, bg=COLOR_WHITE)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        create_button(btn_frame, "Mark Attendance", self.mark_attendance, width=15).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Delete Record", self.delete_attendance, width=15).pack(side=tk.LEFT, padx=5)
        
        self.var_filter = tk.StringVar(value=date.today().strftime("%Y-%m"))
        tk.Entry(btn_frame, textvariable=self.var_filter, font=FONT_BODY, width=15).pack(side=tk.LEFT, padx=20)
        create_button(btn_frame, "Filter by Month", self.load_data, width=15).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        setup_treeview_style()
        cols = ("ID", "Date", "Student Name", "Roll No", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.get_cursor_data)

    def load_students(self):
        query = "SELECT id, name, roll_number FROM students"
        rows = db.fetch_all(query)
        self.student_map = {f"{r['name']} ({r['roll_number']})": r['id'] for r in rows}
        self.combo_student['values'] = list(self.student_map.keys())

    def load_data(self):
        month_filter = f"{self.var_filter.get()}%"
        query = '''
            SELECT a.id, a.date, s.name, s.roll_number, a.status 
            FROM attendance a 
            JOIN students s ON a.student_id = s.id 
            WHERE a.date LIKE %s
            ORDER BY a.date DESC
        '''
        rows = db.fetch_all(query, (month_filter,))
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=(row['id'], row['date'], row['name'], row['roll_number'], row['status']))

    def mark_attendance(self):
        student_key = self.var_student.get()
        if not student_key or not self.var_date.get() or not self.var_status.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
            
        student_id = self.student_map.get(student_key)
        
        # Check if exists
        check_query = "SELECT id FROM attendance WHERE student_id=%s AND date=%s"
        existing = db.fetch_one(check_query, (student_id, self.var_date.get()))
        
        if existing:
            query = "UPDATE attendance SET status=%s WHERE id=%s"
            params = (self.var_status.get(), existing['id'])
        else:
            query = "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)"
            params = (student_id, self.var_date.get(), self.var_status.get())
            
        if db.execute_query(query, params):
            messagebox.showinfo("Success", "Attendance recorded")
            self.load_data()

    def delete_attendance(self):
        if not self.var_id.get(): return
        if db.execute_query("DELETE FROM attendance WHERE id=%s", (self.var_id.get(),)):
            self.var_id.set("")
            self.load_data()

    def get_cursor_data(self, event):
        cursor_row = self.tree.focus()
        if not cursor_row: return
        content = self.tree.item(cursor_row)
        row = content['values']
        if row:
            self.var_id.set(row[0])
            self.var_date.set(row[1])
            student_key = f"{row[2]} ({row[3]})"
            if student_key in self.student_map:
                self.var_student.set(student_key)
            self.var_status.set(row[4])
