# src/gui/gui.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
from parser.log_parser import (
    parse_tc_info, parse_tc_integration_info, parse_tc_aw_variables,
    parse_tc_environment_data, parse_nx_info, parse_nx_config_info
)
from parser.exporter import export_to_excel
from gui.sysinfo_gui import add_system_info_button  # Import the new function
from gui.license_info_gui import add_license_info_button  # Import the new function
from gui.performance_metrics_gui import add_performance_metrics_button  # Import the new function
from gui.installation_info_gui import add_installation_info_button  # Import the new function

class LogFileAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Logfile Analyzer")
        self.geometry("600x400")
        self._create_widgets()

    def _create_widgets(self):
        file_frame = tk.Frame(self)
        file_frame.pack(pady=10)
        
        self.label = tk.Label(file_frame, text="Log file:")
        self.label.pack(side=tk.LEFT, padx=5)
        
        self.file_entry = tk.Entry(file_frame, width=40)
        self.file_entry.pack(side=tk.LEFT, padx=5)

        self.browse_button = tk.Button(file_frame, text="Browse", command=self.select_log_file)
        self.browse_button.pack(side=tk.LEFT, padx=5)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=20)

        add_system_info_button(self.button_frame, self)  # Add the new button function
        add_license_info_button(self.button_frame, self)  # Add the new button function
        add_performance_metrics_button(self.button_frame, self)  # Add the new button function
        add_installation_info_button(self.button_frame, self)  # Add the new button function

        self.tc_info_button = tk.Button(self.button_frame, text="TC Info", command=self.show_tc_info)
        self.tc_info_button.grid(row=1, column=0, padx=10, pady=10)

        self.nx_info_button = tk.Button(self.button_frame, text="NX Info", command=self.show_nx_info)
        self.nx_info_button.grid(row=1, column=1, padx=10, pady=10)

        cc_logo_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'Cc-by-nc-sa_icon.png')
        if os.path.exists(cc_logo_path):
            cc_logo_image = Image.open(cc_logo_path)
            cc_logo_image.thumbnail((50, 50), Image.LANCZOS)
            self.cc_logo = ImageTk.PhotoImage(cc_logo_image)

            self.bottom_frame = tk.Frame(self)
            self.bottom_frame.pack(side=tk.BOTTOM, anchor='w', pady=10, padx=10)

            self.cc_logo_label = tk.Label(self.bottom_frame, image=self.cc_logo)
            self.cc_logo_label.pack(side=tk.LEFT)

            copyright_text = "© Marc Weidner"
            self.copyright_label = tk.Label(self.bottom_frame, text=copyright_text)
            self.copyright_label.pack(side=tk.LEFT, padx=5)

    def select_log_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, self.file_path)

    def show_tc_info(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

        self.show_tc_window()

    def show_tc_window(self):
        tc_window = Toplevel(self)
        tc_window.title("TC Information")
        tc_window.geometry("400x300")

        tc_button = tk.Button(tc_window, text="TC Integration", command=self.show_tc_integration_info)
        tc_button.pack(pady=10)

        tc_variables_button = tk.Button(tc_window, text="TC Variables", command=self.show_tc_aw_variables_info)
        tc_variables_button.pack(pady=10)

        tc_environment_data_button = tk.Button(tc_window, text="TC Environment Data", command=self.show_tc_environment_data)
        tc_environment_data_button.pack(pady=10)

    def show_tc_integration_info(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

        tc_integration_info = parse_tc_integration_info(self.file_path)
        self.show_results(tc_integration_info, "TC Integration Information")

    def show_tc_aw_variables_info(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

        tc_aw_variables_info = parse_tc_aw_variables(self.file_path)
        self.show_results(tc_aw_variables_info, "TC Variables Information")

    def show_tc_environment_data(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

        tc_environment_data = parse_tc_environment_data(self.file_path)
        self.show_results(tc_environment_data, "TC Environment Data")

    def show_nx_info(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

        self.show_nx_window()

    def show_nx_window(self):
        nx_window = Toplevel(self)
        nx_window.title("NX Information")
        nx_window.geometry("400x300")

        nx_config_button = tk.Button(nx_window, text="NX Configuration Variables", command=self.show_nx_config_info)
        nx_config_button.pack(pady=10)

        nx_system_env_button = tk.Button(nx_window, text="NX System Environment Variables", command=self.show_nx_system_env_info)
        nx_system_env_button.pack(pady=10)

        nx_used_env_files_button = tk.Button(nx_window, text="NX used env files", command=self.show_nx_used_env_files_info)
        nx_used_env_files_button.pack(pady=10)

    def show_nx_config_info(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

        nx_config_info = parse_nx_config_info(self.file_path)
        self.show_results(nx_config_info, "NX Configuration Variables")

    def show_nx_system_env_info(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

    def show_nx_used_env_files_info(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

    def show_results(self, info_list, title):
        result_window = Toplevel(self)
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

        export_button = tk.Button(result_window, text="Export to Excel", command=lambda: self.export_to_excel(info_list, title))
        export_button.pack(pady=10)

        result_window.update_idletasks()
        result_window.minsize(result_window.winfo_reqwidth(), result_window.winfo_reqheight())

    def _get_icon_path(self):
        return os.path.join(os.path.dirname(__file__), '..', 'images', 'logo.ico')

    def export_to_excel(self, data, title):
        import pandas as pd

        with pd.ExcelWriter(f"{title}.xlsx") as writer:
            df = pd.DataFrame(data, columns=["Key", "Value"])
            df.to_excel(writer, sheet_name=title[:30])

        messagebox.showinfo("Export Successful", f"Data exported to {title}.xlsx")

if __name__ == "__main__":
    app = LogFileAnalyzerApp()
    app.mainloop()
