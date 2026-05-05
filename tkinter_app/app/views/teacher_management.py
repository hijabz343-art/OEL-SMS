import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import *
from app.services.db_service import db

class TeacherManagementView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_WHITE)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        create_header(self, "Teacher Management").pack(fill=tk.X)

        form_frame = tk.Frame(self, bg=COLOR_WHITE, pady=10)
        form_frame.pack(fill=tk.X, padx=20)

        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_subject = tk.StringVar()
        self.var_contact = tk.StringVar()
        self.var_salary = tk.StringVar()

        fields = [
            ("Name:", self.var_name, 0, 0),
            ("Subject:", self.var_subject, 0, 2),
            ("Contact:", self.var_contact, 1, 0),
            ("Salary:", self.var_salary, 1, 2)
        ]

        for text, var, r, c in fields:
            create_label(form_frame, text).grid(row=r, column=c, padx=5, pady=5, sticky=tk.W)
            tk.Entry(form_frame, textvariable=var, font=FONT_BODY, width=25).grid(row=r, column=c+1, padx=5, pady=5)

        btn_frame = tk.Frame(self, bg=COLOR_WHITE)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        create_button(btn_frame, "Add", self.add_teacher, width=10).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Update", self.update_teacher, width=10).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Delete", self.delete_teacher, width=10).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Clear", self.clear_form, width=10).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        setup_treeview_style()
        cols = ("ID", "Name", "Subject", "Contact", "Salary")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.get_cursor_data)

    def load_data(self):
        query = "SELECT * FROM teachers"
        rows = db.fetch_all(query)
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=(row['id'], row['name'], row['subject'], row['contact'], row['salary']))

    def add_teacher(self):
        if not self.validate_input(): return
        query = "INSERT INTO teachers (name, subject, contact, salary) VALUES (%s, %s, %s, %s)"
        params = (self.var_name.get(), self.var_subject.get(), self.var_contact.get(), self.var_salary.get())
        if db.execute_query(query, params):
            messagebox.showinfo("Success", "Teacher added successfully")
            self.clear_form()
            self.load_data()

    def update_teacher(self):
        if not self.var_id.get(): return
        query = "UPDATE teachers SET name=%s, subject=%s, contact=%s, salary=%s WHERE id=%s"
        params = (self.var_name.get(), self.var_subject.get(), self.var_contact.get(), self.var_salary.get(), self.var_id.get())
        if db.execute_query(query, params):
            messagebox.showinfo("Success", "Teacher updated successfully")
            self.clear_form()
            self.load_data()

    def delete_teacher(self):
        if not self.var_id.get(): return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this teacher?"):
            query = "DELETE FROM teachers WHERE id=%s"
            if db.execute_query(query, (self.var_id.get(),)):
                self.clear_form()
                self.load_data()

    def clear_form(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_subject.set("")
        self.var_contact.set("")
        self.var_salary.set("")

    def get_cursor_data(self, event):
        cursor_row = self.tree.focus()
        if not cursor_row: return
        content = self.tree.item(cursor_row)
        row = content['values']
        self.var_id.set(row[0])
        self.var_name.set(row[1])
        self.var_subject.set(row[2])
        self.var_contact.set(row[3])
        self.var_salary.set(row[4])

    def validate_input(self):
        if not all([self.var_name.get(), self.var_subject.get(), self.var_salary.get()]):
            messagebox.showerror("Error", "Required fields cannot be empty")
            return False
        return True
