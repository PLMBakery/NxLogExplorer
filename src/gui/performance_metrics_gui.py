# src/gui/performance_metrics_gui.py

import tkinter as tk
from tkinter import messagebox, Toplevel
from parser.performance_metrics_parser import parse_performance_metrics

def add_performance_metrics_button(frame, app):
    performance_button = tk.Button(frame, text="Performance Metrics", command=lambda: show_performance_metrics(app))
    performance_button.grid(row=0, column=2, padx=10, pady=10)

def show_performance_metrics(app):
    if not hasattr(app, 'file_path') or not app.file_path:
        messagebox.showerror("No file selected", "Please select a log file first.")
        return

    performance_metrics = parse_performance_metrics(app.file_path)
    show_results(app, performance_metrics, "Performance Metrics")

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
