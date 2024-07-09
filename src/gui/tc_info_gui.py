# src/gui/tc_info_gui.py

import tkinter as tk
from tkinter import messagebox, Toplevel
from parser.tc_info_parser import (
    parse_tc_info, parse_tc_integration_info,
    parse_tc_aw_variables, parse_tc_environment_data
)

def add_tc_info_button(frame, app):
    tc_info_button = tk.Button(frame, text="TC Info", command=lambda: show_tc_info(app))
    tc_info_button.grid(row=1, column=0, padx=10, pady=10)

def show_tc_info(app):
    if not hasattr(app, 'file_path') or not app.file_path:
        messagebox.showerror("No file selected", "Please select a log file first.")
        return

    show_tc_window(app)

def show_tc_window(app):
    tc_window = Toplevel(app)
    tc_window.title("TC Information")
    tc_window.geometry("400x300")

    tc_button = tk.Button(tc_window, text="TC Integration", command=lambda: show_tc_integration_info(app))
    tc_button.pack(pady=10)

    tc_variables_button = tk.Button(tc_window, text="TC Variables", command=lambda: show_tc_aw_variables_info(app))
    tc_variables_button.pack(pady=10)

    tc_environment_data_button = tk.Button(tc_window, text="TC Environment Data", command=lambda: show_tc_environment_data(app))
    tc_environment_data_button.pack(pady=10)

def show_tc_integration_info(app):
    if not hasattr(app, 'file_path') or not app.file_path:
        messagebox.showerror("No file selected", "Please select a log file first.")
        return

    tc_integration_info = parse_tc_integration_info(app.file_path)
    show_results(app, tc_integration_info, "TC Integration Information")

def show_tc_aw_variables_info(app):
    if not hasattr(app, 'file_path') or not app.file_path:
        messagebox.showerror("No file selected", "Please select a log file first.")
        return

    tc_aw_variables_info = parse_tc_aw_variables(app.file_path)
    show_results(app, tc_aw_variables_info, "TC Variables Information")

def show_tc_environment_data(app):
    if not hasattr(app, 'file_path') or not app.file_path:
        messagebox.showerror("No file selected", "Please select a log file first.")
        return

    tc_environment_data = parse_tc_environment_data(app.file_path)
    show_results(app, tc_environment_data, "TC Environment Data")

def show_results(app, info_list, title):
    result_window = Toplevel(app)
    result_window.title(title)

    title_label = tk.Label(result_window, text=title, font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    result_frame = tk.Frame(result_window)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(result_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget = tk.Text(result_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text_widget.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_widget.yview)

    text_widget.tag_configure("bold", font=("Arial", 10, "bold"))

    for attribute, value in info_list:
        text_widget.insert(tk.END, f"{attribute}:\n", "bold")
        text_widget.insert(tk.END, f"{value}\n\n")

    result_window.update_idletasks()
    result_window.minsize(result_window.winfo_reqwidth(), result_window.winfo_reqheight())
