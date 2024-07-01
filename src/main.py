import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Text, Scrollbar, RIGHT, Y, END
from PIL import Image, ImageTk
import os
import pandas as pd

class LogFileAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        try:
            # Set the title of the main window
            self.title("Logfile Analyzer")
            # Set the size of the main window
            self.geometry("400x300")
            # Set the icon for the taskbar
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'logo.ico')
            self.iconbitmap(icon_path)
            # Create and arrange the widgets in the main window
            self._create_widgets()
        except Exception as e:
            print(f"Error during initialization: {e}")

    def _create_widgets(self):
        try:
            # Create a frame for file selection
            file_frame = tk.Frame(self)
            file_frame.pack(pady=10)
            
            # Create and pack a label widget
            self.label = tk.Label(file_frame, text="Log file:")
            self.label.pack(side=tk.LEFT, padx=5)
            
            # Create and pack an entry widget for the file path
            self.file_entry = tk.Entry(file_frame, width=40)
            self.file_entry.pack(side=tk.LEFT, padx=5)

            # Create and pack a button widget to select a log file
            self.browse_button = tk.Button(file_frame, text="Browse", command=self.select_log_file)
            self.browse_button.pack(side=tk.LEFT, padx=5)

            # Create a frame to hold placeholder buttons
            self.button_frame = tk.Frame(self)
            self.button_frame.pack(pady=20)

            # Create and arrange six buttons, using Button 1 for analyzing loading times
            self.analyze_button = tk.Button(self.button_frame, text="Analyze Loading Times", command=self.analyze_loading_times)
            self.analyze_button.grid(row=0, column=0, padx=10, pady=10)

            for i in range(1, 6):
                btn = tk.Button(self.button_frame, text=f"Button {i+1}", state=tk.DISABLED)
                btn.grid(row=i//3, column=i%3, padx=10, pady=10)

            # Load CC BY-NC-SA license logo image
            cc_logo_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'Cc-by-nc-sa_icon.png')
            if os.path.exists(cc_logo_path):
                cc_logo_image = Image.open(cc_logo_path)
                cc_logo_image.thumbnail((50, 50), Image.LANCZOS)
                self.cc_logo = ImageTk.PhotoImage(cc_logo_image)

                # Create a frame to hold the logo and text
                self.bottom_frame = tk.Frame(self)
                self.bottom_frame.pack(side=tk.BOTTOM, anchor='w', pady=10, padx=10)

                # Create a label widget for the CC BY-NC-SA license logo
                self.cc_logo_label = tk.Label(self.bottom_frame, image=self.cc_logo)
                self.cc_logo_label.pack(side=tk.LEFT)

                # Create a label widget for the copyright text
                self.copyright_label = tk.Label(self.bottom_frame, text="© Marc Weidner")
                self.copyright_label.pack(side=tk.LEFT, padx=5)

        except Exception as e:
            print(f"Error during widget creation: {e}")

    def select_log_file(self):
        try:
            # Open a file dialog to select a log file
            self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if self.file_path:
                # Update the entry with the selected file path
                self.file_entry.delete(0, tk.END)
                self.file_entry.insert(0, self.file_path)
        except Exception as e:
            print(f"Error during file selection: {e}")

    def analyze_loading_times(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("No file selected", "Please select a log file first.")
            return

        load_times, operations = self.parse_log_file(self.file_path)
        self.show_results(load_times, operations)

    def parse_log_file(self, file_path):
        load_times = []
        operations = []
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if "Loaded and updated part" in line or "Performed operation" in line:
                parts = line.split()
                if len(parts) >= 6 and parts[-2] == 'real':
                    time = float(parts[-1])
                    load_times.append(time)
                    operations.append(line.strip())
        
        return load_times, operations

    def show_results(self, load_times, operations):
        result_window = Toplevel(self)
        result_window.title("Loading Times Analysis")
        result_window.geometry("600x400")

        text_area = Text(result_window)
        scroll_bar = Scrollbar(result_window, command=text_area.yview)
        text_area.configure(yscrollcommand=scroll_bar.set)

        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_bar.pack(side=RIGHT, fill=Y)

        text_area.insert(END, "Loading Times Analysis Results\n\n")
        for operation, time in zip(operations, load_times):
            text_area.insert(END, f"{operation} - Time: {time}\n")

        export_button = tk.Button(result_window, text="Export to Excel", command=lambda: self.export_to_excel(load_times, operations))
        export_button.pack(pady=10)

    def export_to_excel(self, load_times, operations):
        df = pd.DataFrame({
            "Operation": operations,
            "Time": load_times
        })
        output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if output_path:
            df.to_excel(output_path, index=False)
            messagebox.showinfo("Export Complete", f"Data exported to {output_path}")

if __name__ == "__main__":
    # Create an instance of the application and run it
    app = LogFileAnalyzerApp()
    app.mainloop()
