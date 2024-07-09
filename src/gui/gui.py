# src/gui/gui.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
from parser.exporter import export_to_excel
from gui.sysinfo_gui import add_system_info_button
from gui.license_info_gui import add_license_info_button
from gui.performance_metrics_gui import add_performance_metrics_button
from gui.installation_info_gui import add_installation_info_button
from gui.tc_info_gui import add_tc_info_button
from gui.nx_info_gui import add_nx_info_button

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

        add_system_info_button(self.button_frame, self)
        add_license_info_button(self.button_frame, self)
        add_performance_metrics_button(self.button_frame, self)
        add_installation_info_button(self.button_frame, self)
        add_tc_info_button(self.button_frame, self)
        add_nx_info_button(self.button_frame, self)

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
