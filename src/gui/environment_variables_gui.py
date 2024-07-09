# src/gui/environment_variables_gui.py

import tkinter as tk
from tkinter import messagebox, Toplevel
from parser.environment_variables_parser import parse_environment_variables

def add_environment_variables_button(frame, app):
    env_button = tk.Button(frame, text="Environment Variables", command=lambda: show_environment_variables(app))
    env_button.grid(row=2, column=0, padx=10, pady=10)

def show_environment_variables(app):
    if not hasattr(app, 'file_path') or not app.file_path:
        messagebox.showerror("No file selected", "Please select a log file first.")
        return

    environment_data = parse_environment_variables(app.file_path)
    show_results(app, environment_data, "System Environment Variables")

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

    for variable, value in info_list:
        text_widget.insert(tk.END, f"Variable: {variable}\n", "bold")
        text_widget.insert(tk.END, f"Value: {value}\n\n")

    result_window.update_idletasks()
    result_window.minsize(result_window.winfo_reqwidth(), result_window.winfo_reqheight())
