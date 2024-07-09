# src/gui/nx_info_gui.py

import tkinter as tk
from tkinter import messagebox, Toplevel
from parser.nx_info_parser import parse_nx_config_info
from parser.environment_variables_parser import parse_environment_variables  # Import the parser

def add_nx_info_button(frame, app):
    nx_info_button = tk.Button(frame, text="NX Info", command=lambda: show_nx_info(app))
    nx_info_button.grid(row=1, column=1, padx=10, pady=10)

def show_nx_info(app):
    if not hasattr(app, 'file_path') or not app.file_path:
        messagebox.showerror("No file selected", "Please select a log file first.")
        return

    show_nx_window(app)

def show_nx_window(app):
    nx_window = Toplevel(app)
    nx_window.title("NX Information")
    nx_window.geometry("600x400")

    nx_config_button = tk.Button(nx_window, text="NX Configuration Variables", command=lambda: show_nx_config_info(app))
    nx_config_button.pack(pady=10)

    # Adding the new button for Environment Variables
    env_vars_button = tk.Button(nx_window, text="NX Environment Variables", command=lambda: show_environment_variables(app))
    env_vars_button.pack(pady=10)

def show_nx_config_info(app):
    if not hasattr(app, 'file_path') or not app.file_path:
        messagebox.showerror("No file selected", "Please select a log file first.")
        return

    nx_config_info = parse_nx_config_info(app.file_path)
    show_results(app, nx_config_info, "NX Configuration Variables", has_location=True)

def show_environment_variables(app):
    if not hasattr(app, 'file_path') or not app.file_path:
        messagebox.showerror("No file selected", "Please select a log file first.")
        return

    environment_data = parse_environment_variables(app.file_path)
    show_results(app, environment_data, "System Environment Variables")

def show_results(app, info_list, title, has_location=False):
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

    for item in info_list:
        if has_location:
            variable, value, location = item
            text_widget.insert(tk.END, f"Variable: {variable}\n", "bold")
            text_widget.insert(tk.END, f"Value: {value}\n")
            text_widget.insert(tk.END, f"Location: {location}\n\n")
        else:
            variable, value = item
            text_widget.insert(tk.END, f"Variable: {variable}\n", "bold")
            text_widget.insert(tk.END, f"Value: {value}\n\n")

    result_window.update_idletasks()
    result_window.minsize(result_window.winfo_reqwidth(), result_window.winfo_reqheight())
