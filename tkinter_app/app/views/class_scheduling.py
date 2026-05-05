import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import *
from app.services.db_service import db

class ClassSchedulingView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_WHITE)
        self.teacher_map = {} # Maps teacher name to ID
        self.create_widgets()
        self.load_teachers()
        self.load_data()

    def create_widgets(self):
        create_header(self, "Class Scheduling").pack(fill=tk.X)

        form_frame = tk.Frame(self, bg=COLOR_WHITE, pady=10)
        form_frame.pack(fill=tk.X, padx=20)

        self.var_id = tk.StringVar()
        self.var_class = tk.StringVar()
        self.var_teacher = tk.StringVar()
        self.var_subject = tk.StringVar()

        create_label(form_frame, "Class Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(form_frame, textvariable=self.var_class, font=FONT_BODY, width=25).grid(row=0, column=1, padx=5, pady=5)

        create_label(form_frame, "Subject:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        tk.Entry(form_frame, textvariable=self.var_subject, font=FONT_BODY, width=25).grid(row=0, column=3, padx=5, pady=5)

        create_label(form_frame, "Teacher:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.teacher_combo = ttk.Combobox(form_frame, textvariable=self.var_teacher, font=FONT_BODY, width=23, state="readonly")
        self.teacher_combo.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self, bg=COLOR_WHITE)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        create_button(btn_frame, "Assign", self.assign_class, width=10).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Delete", self.delete_class, width=10).pack(side=tk.LEFT, padx=5)
        create_button(btn_frame, "Clear", self.clear_form, width=10).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        setup_treeview_style()
        cols = ("ID", "Class Name", "Subject", "Teacher Name")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.get_cursor_data)

    def load_teachers(self):
        query = "SELECT id, name FROM teachers"
        rows = db.fetch_all(query)
        self.teacher_map = {row['name']: row['id'] for row in rows}
        self.teacher_combo['values'] = list(self.teacher_map.keys())

    def load_data(self):
        query = '''
            SELECT c.id, c.class_name, c.subject, t.name as teacher_name 
            FROM classes c 
            LEFT JOIN teachers t ON c.teacher_id = t.id
        '''
        rows = db.fetch_all(query)
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=(row['id'], row['class_name'], row['subject'], row['teacher_name']))

    def assign_class(self):
        teacher_name = self.var_teacher.get()
        if not teacher_name or not self.var_class.get() or not self.var_subject.get():
            messagebox.showerror("Error", "All fields are required")
            return
            
        teacher_id = self.teacher_map.get(teacher_name)
        
        if self.var_id.get():
            query = "UPDATE classes SET class_name=%s, subject=%s, teacher_id=%s WHERE id=%s"
            params = (self.var_class.get(), self.var_subject.get(), teacher_id, self.var_id.get())
        else:
            query = "INSERT INTO classes (class_name, subject, teacher_id) VALUES (%s, %s, %s)"
            params = (self.var_class.get(), self.var_subject.get(), teacher_id)
            
        if db.execute_query(query, params):
            messagebox.showinfo("Success", "Class assignment saved")
            self.clear_form()
            self.load_data()

    def delete_class(self):
        if not self.var_id.get(): return
        if messagebox.askyesno("Confirm", "Delete this assignment?"):
            if db.execute_query("DELETE FROM classes WHERE id=%s", (self.var_id.get(),)):
                self.clear_form()
                self.load_data()

    def clear_form(self):
        self.var_id.set("")
        self.var_class.set("")
        self.var_subject.set("")
        self.var_teacher.set("")

    def get_cursor_data(self, event):
        cursor_row = self.tree.focus()
        if not cursor_row: return
        content = self.tree.item(cursor_row)
        row = content['values']
        if row:
            self.var_id.set(row[0])
            self.var_class.set(row[1])
            self.var_subject.set(row[2])
            self.var_teacher.set(row[3])
