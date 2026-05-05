import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import *
from app.services.db_service import db

class StudentRegistrationView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_WHITE)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        create_header(self, "Student Registration").pack(fill=tk.X)
        self.create_form_widgets()
        self.create_button_widgets()
        self.create_tree_widgets()

    def create_form_widgets(self):
        form_frame = tk.Frame(self, bg=COLOR_WHITE, pady=10)
        form_frame.pack(fill=tk.X, padx=20)

        # Variables
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_roll = tk.StringVar()
        self.var_class = tk.StringVar()
        self.var_dob = tk.StringVar()
        self.var_contact = tk.StringVar()

        # Labels & Entries
        fields = [
            ("Name:", self.var_name, 0, 0),
            ("Roll Number:", self.var_roll, 0, 2),
            ("Class:", self.var_class, 1, 0),
            ("DOB (YYYY-MM-DD):", self.var_dob, 1, 2),
            ("Parent Contact:", self.var_contact, 2, 0)
        ]

        for text, var, r, c in fields:
            create_label(form_frame, text).grid(row=r, column=c, padx=5, pady=5, sticky=tk.W)
            tk.Entry(form_frame, textvariable=var, font=FONT_BODY, width=25).grid(row=r, column=c+1, padx=5, pady=5)

    def create_button_widgets(self):
        btn_frame = tk.Frame(self, bg=COLOR_WHITE)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        create_button(btn_frame, "Add", self.add_student, width=10).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Update", self.update_student, width=10).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Delete", self.delete_student, width=10).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Clear", self.clear_form, width=10).pack(side=tk.LEFT, padx=5)
        
        self.var_search = tk.StringVar()
        tk.Entry(btn_frame, textvariable=self.var_search, font=FONT_BODY, width=20).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Search", self.search_student, width=10).pack(side=tk.LEFT, padx=5)

    def create_tree_widgets(self):
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        setup_treeview_style()
        cols = ("ID", "Name", "Roll No", "Class", "DOB", "Contact")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.get_cursor_data)

    def load_data(self):
        query = "SELECT * FROM students"
        rows = db.fetch_all(query)
        self.update_tree(rows)

    def update_tree(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=(row['id'], row['name'], row['roll_number'], row['class_name'], row['dob'], row['parent_contact']))

    def add_student(self):
        if not self.validate_input(): return
        query = "INSERT INTO students (name, roll_number, class_name, dob, parent_contact) VALUES (%s, %s, %s, %s, %s)"
        params = (self.var_name.get(), self.var_roll.get(), self.var_class.get(), self.var_dob.get(), self.var_contact.get())
        if db.execute_query(query, params):
            messagebox.showinfo("Success", "Student added successfully")
            self.clear_form()
            self.load_data()

    def update_student(self):
        if not self.var_id.get():
            messagebox.showerror("Error", "Please select a student from the list")
            return
        query = "UPDATE students SET name=%s, roll_number=%s, class_name=%s, dob=%s, parent_contact=%s WHERE id=%s"
        params = (self.var_name.get(), self.var_roll.get(), self.var_class.get(), self.var_dob.get(), self.var_contact.get(), self.var_id.get())
        if db.execute_query(query, params):
            messagebox.showinfo("Success", "Student updated successfully")
            self.clear_form()
            self.load_data()

    def delete_student(self):
        if not self.var_id.get(): return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            query = "DELETE FROM students WHERE id=%s"
            if db.execute_query(query, (self.var_id.get(),)):
                self.clear_form()
                self.load_data()

    def search_student(self):
        search_term = f"%{self.var_search.get()}%"
        query = "SELECT * FROM students WHERE name LIKE %s OR roll_number LIKE %s"
        rows = db.fetch_all(query, (search_term, search_term))
        self.update_tree(rows)

    def clear_form(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_roll.set("")
        self.var_class.set("")
        self.var_dob.set("")
        self.var_contact.set("")

    def get_cursor_data(self, event):
        cursor_row = self.tree.focus()
        if not cursor_row: return
        content = self.tree.item(cursor_row)
        row = content['values']
        self.var_id.set(row[0])
        self.var_name.set(row[1])
        self.var_roll.set(row[2])
        self.var_class.set(row[3])
        self.var_dob.set(row[4])
        self.var_contact.set(row[5])

    def validate_input(self):
        if not all([self.var_name.get(), self.var_roll.get(), self.var_class.get(), self.var_dob.get()]):
            messagebox.showerror("Error", "All required fields must be filled")
            return False
        return True
