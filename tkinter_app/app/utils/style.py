import tkinter as tk
from tkinter import ttk

# Constants
COLOR_NAVY_BLUE = "#1B3A6B"
COLOR_WHITE = "#FFFFFF"
COLOR_ORANGE = "#FF8C00"
COLOR_LIGHT_GRAY = "#F0F0F0"

FONT_BODY = ("Arial", 11)
FONT_HEADING = ("Arial", 14, "bold")
FONT_TITLE = ("Arial", 20, "bold")

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

def create_main_window(title="School Management System"):
    """Creates and configures the main Tkinter window."""
    root = tk.Tk()
    root.title(title)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.configure(bg=COLOR_WHITE)
    return root

def create_header(parent, text):
    """Creates a standardized navy blue header label."""
    header = tk.Label(
        parent,
        text=text,
        bg=COLOR_NAVY_BLUE,
        fg=COLOR_WHITE,
        font=FONT_TITLE,
        pady=10
    )
    return header

def create_button(parent, text, command, width=15):
    """Creates a standardized orange button."""
    btn = tk.Button(
        parent,
        text=text,
        bg=COLOR_ORANGE,
        fg=COLOR_WHITE,
        font=FONT_BODY,
        command=command,
        width=width,
        relief=tk.FLAT,
        cursor="hand2"
    )
    return btn

def create_label(parent, text, font=FONT_BODY):
    """Creates a standard white background label."""
    return tk.Label(parent, text=text, bg=COLOR_WHITE, font=font)

def create_entry(parent, width=30):
    """Creates a standard entry widget."""
    return tk.Entry(parent, font=FONT_BODY, width=width)

def setup_treeview_style():
    """Configures the ttk Treeview style."""
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "Treeview",
        background=COLOR_WHITE,
        foreground="black",
        rowheight=25,
        fieldbackground=COLOR_WHITE,
        font=FONT_BODY
    )
    style.configure("Treeview.Heading", font=FONT_HEADING, background=COLOR_LIGHT_GRAY)
    style.map("Treeview", background=[('selected', COLOR_NAVY_BLUE)])
