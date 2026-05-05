import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from app.utils.style import *
from app.services.db_service import db

class FeeManagementView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_WHITE)
        self.student_map = {}
        self.create_widgets()
        self.load_students()
        self.load_data()

    def create_widgets(self):
        create_header(self, "Fee Management").pack(fill=tk.X)

        form_frame = tk.Frame(self, bg=COLOR_WHITE, pady=10)
        form_frame.pack(fill=tk.X, padx=20)

        self.var_id = tk.StringVar()
        self.var_student = tk.StringVar()
        self.var_amount = tk.StringVar()
        self.var_status = tk.StringVar(value="Pending")

        create_label(form_frame, "Student:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_student = ttk.Combobox(form_frame, textvariable=self.var_student, font=FONT_BODY, width=25, state="readonly")
        self.combo_student.grid(row=0, column=1, padx=5, pady=5)

        create_label(form_frame, "Amount:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        tk.Entry(form_frame, textvariable=self.var_amount, font=FONT_BODY, width=20).grid(row=0, column=3, padx=5, pady=5)

        create_label(form_frame, "Status:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_status = ttk.Combobox(form_frame, textvariable=self.var_status, font=FONT_BODY, width=25, state="readonly")
        self.combo_status['values'] = ("Pending", "Paid")
        self.combo_status.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self, bg=COLOR_WHITE)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        create_button(btn_frame, "Record Fee", self.record_fee, width=15).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Mark as Paid", self.mark_paid, width=15).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Delete", self.delete_fee, width=15).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Clear", self.clear_form, width=15).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        setup_treeview_style()
        cols = ("ID", "Student Name", "Roll No", "Amount", "Status", "Paid Date")
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
        query = '''
            SELECT f.id, s.name, s.roll_number, f.amount, f.status, f.paid_date 
            FROM fees f 
            JOIN students s ON f.student_id = s.id
        '''
        rows = db.fetch_all(query)
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=(row['id'], row['name'], row['roll_number'], row['amount'], row['status'], row['paid_date'] or "-"))

    def record_fee(self):
        student_key = self.var_student.get()
        if not student_key or not self.var_amount.get():
            messagebox.showerror("Error", "Student and Amount are required")
            return
            
        student_id = self.student_map.get(student_key)
        paid_date = date.today().strftime("%Y-%m-%d") if self.var_status.get() == "Paid" else None
        
        if self.var_id.get():
            query = "UPDATE fees SET student_id=%s, amount=%s, status=%s, paid_date=%s WHERE id=%s"
            params = (student_id, self.var_amount.get(), self.var_status.get(), paid_date, self.var_id.get())
        else:
            query = "INSERT INTO fees (student_id, amount, status, paid_date) VALUES (%s, %s, %s, %s)"
            params = (student_id, self.var_amount.get(), self.var_status.get(), paid_date)
            
        if db.execute_query(query, params):
            self.clear_form()
            self.load_data()

    def mark_paid(self):
        if not self.var_id.get():
            messagebox.showwarning("Warning", "Select a fee record first")
            return
            
        paid_date = date.today().strftime("%Y-%m-%d")
        query = "UPDATE fees SET status='Paid', paid_date=%s WHERE id=%s"
        if db.execute_query(query, (paid_date, self.var_id.get())):
            messagebox.showinfo("Success", "Receipt generated! Fee marked as paid.")
            self.clear_form()
            self.load_data()

    def delete_fee(self):
        if not self.var_id.get(): return
        if db.execute_query("DELETE FROM fees WHERE id=%s", (self.var_id.get(),)):
            self.clear_form()
            self.load_data()

    def clear_form(self):
        self.var_id.set("")
        self.var_student.set("")
        self.var_amount.set("")
        self.var_status.set("Pending")

    def get_cursor_data(self, event):
        cursor_row = self.tree.focus()
        if not cursor_row: return
        content = self.tree.item(cursor_row)
        row = content['values']
        if row:
            self.var_id.set(row[0])
            student_key = f"{row[1]} ({row[2]})"
            if student_key in self.student_map:
                self.var_student.set(student_key)
            self.var_amount.set(row[3])
            self.var_status.set(row[4])
