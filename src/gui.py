import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
import os
from log_parser import parse_system_info, parse_license_info, parse_performance_metrics, parse_installation_info
from exporter import export_to_excel

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

        self.system_info_button = tk.Button(self.button_frame, text="System Information", command=self.show_system_info)
        self.system_info_button.grid(row=0, column=0, padx=10, pady=10)

        self.license_info_button = tk.Button(self.button_frame, text="License Information", command=self.show_license_info)
        self.license_info_button.grid(row=0, column=1, padx=10, pady=10)

        self.performance_button = tk.Button(self.button_frame, text="Performance Metrics", command=self.show_performance_metrics)
        self.performance_button.grid(row=0, column=2, padx=10, pady=10)

        self.installation_info_button = tk.Button(self.button_frame, text="Installation Information", command=self.show_installation_info)
        self.installation_info_button.grid(row=0, column=3, padx=10, pady=10)

        cc_logo_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'Cc-by-nc-sa_icon.png')
        if os.path.exists(cc_logo_path):
            cc_logo_image = Image.open(cc_logo_path)
            cc_logo_image.thumbnail((50, 50), Image.LANCZOS)
            self.cc_logo = ImageTk.PhotoImage(cc_logo_image)

            self.bottom_frame = tk.Frame(self)
            self.bottom_frame.pack(side=tk.BOTTOM, anchor='w', pady=10, padx=10)

            self.cc_logo_label = tk.Label(self.bottom_frame, image=self.cc_logo)
            self.cc_logo_label.pack(side=tk.LEFT)

            self.copyright_label = tk.Label(self.bottom_frame, text="© Marc Weidner")
            self.copyright_label.pack(side=tk.LEFT, padx=5)

    def select_log_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, self.file_path)

    def show_system_info(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

        system_info = parse_system_info(self.file_path)
        self.show_results(system_info, "System Information")

    def show_license_info(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

        license_info = parse_license_info(self.file_path)
        self.show_results(license_info, "License Information")

    def show_performance_metrics(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

        performance_metrics = parse_performance_metrics(self.file_path)
        self.show_results(performance_metrics, "Performance Metrics")

    def show_installation_info(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

        installation_info = parse_installation_info(self.file_path)
        self.show_results(installation_info, "Installation Information")

    def show_results(self, info_list, title):
        result_window = Toplevel(self)
        result_window.title(title)
        result_window.iconbitmap(self._get_icon_path())

        title_label = tk.Label(result_window, text=title, font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        result_frame = tk.Frame(result_window)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Hinzufügen einer Scrollbar und eines Text-Widgets für die Anzeige
        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(result_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        # Konfigurieren des Tags für fett gedruckten Text
        text_widget.tag_configure("bold", font=("Arial", 10, "bold"))

        # Formatierung der Ergebnisse und Hinzufügen zum Text-Widget
        for attribute, value in info_list:
            text_widget.insert(tk.END, f"{attribute}:\n", "bold")
            text_widget.insert(tk.END, f"{value}\n\n")

        export_button = tk.Button(result_window, text="Export to Excel", command=lambda: export_to_excel(info_list, title))
        export_button.pack(pady=10)

        result_window.update_idletasks()
        result_window.minsize(result_window.winfo_reqwidth(), result_window.winfo_reqheight())

    def _get_icon_path(self):
        return os.path.join(os.path.dirname(__file__), '..', 'images', 'logo.ico')

if __name__ == "__main__":
    app = LogFileAnalyzerApp()
    app.mainloop()
