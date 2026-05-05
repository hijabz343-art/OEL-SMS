import tkinter as tk
from app.utils.style import *
from app.services.db_service import db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportsDashboardView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_WHITE)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        create_header(self, "Reports Dashboard").pack(fill=tk.X)

        # Cards Frame
        self.cards_frame = tk.Frame(self, bg=COLOR_WHITE, pady=20)
        self.cards_frame.pack(fill=tk.X, padx=20)

        # Chart Frame
        self.chart_frame = tk.Frame(self, bg=COLOR_WHITE)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_card(self, parent, title, value, col):
        card = tk.Frame(parent, bg=COLOR_LIGHT_GRAY, bd=2, relief=tk.RIDGE, padx=20, pady=20)
        card.grid(row=0, column=col, padx=15, sticky=tk.NSEW)
        
        tk.Label(card, text=title, font=FONT_HEADING, bg=COLOR_LIGHT_GRAY).pack()
        tk.Label(card, text=str(value), font=FONT_TITLE, bg=COLOR_LIGHT_GRAY, fg=COLOR_NAVY_BLUE).pack(pady=10)
        parent.grid_columnconfigure(col, weight=1)

    def load_data(self):
        # Clear existing cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
            
        # Get Totals
        students_count = db.fetch_one("SELECT COUNT(*) as c FROM students")['c']
        teachers_count = db.fetch_one("SELECT COUNT(*) as c FROM teachers")['c']
        
        fee_data = db.fetch_one("SELECT SUM(amount) as s FROM fees WHERE status='Paid'")
        total_fees = fee_data['s'] if fee_data['s'] else 0
        
        # Calculate Attendance %
        total_att = db.fetch_one("SELECT COUNT(*) as c FROM attendance")['c']
        present_att = db.fetch_one("SELECT COUNT(*) as c FROM attendance WHERE status='Present'")['c']
        att_percentage = round((present_att / total_att * 100), 2) if total_att > 0 else 0

        self.create_card(self.cards_frame, "Total Students", students_count, 0)
        self.create_card(self.cards_frame, "Total Teachers", teachers_count, 1)
        self.create_card(self.cards_frame, "Fees Collected", f"${total_fees}", 2)
        self.create_card(self.cards_frame, "Attendance %", f"{att_percentage}%", 3)

        self.draw_chart(students_count, teachers_count)

    def draw_chart(self, students, teachers):
        # Clear existing chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        categories = ['Students', 'Teachers']
        counts = [students, teachers]
        
        ax.bar(categories, counts, color=[COLOR_NAVY_BLUE, COLOR_ORANGE])
        ax.set_title('School Demographics')
        ax.set_ylabel('Count')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
