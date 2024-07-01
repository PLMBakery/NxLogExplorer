import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

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
            # Create and pack a label widget
            self.label = tk.Label(self, text="Select a log file:")
            self.label.pack(pady=10)

            # Create and pack a button widget to select a log file
            self.select_button = tk.Button(self, text="Select Log File", command=self.select_log_file)
            self.select_button.pack(pady=5)

            # Create a frame to hold placeholder buttons
            self.button_frame = tk.Frame(self)
            self.button_frame.pack(pady=20)

            # Create and arrange six disabled placeholder buttons
            for i in range(6):
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
                self.copyright_label = tk.Label(self.bottom_frame, text="© by Marc Weidner")
                self.copyright_label.pack(side=tk.LEFT, padx=5)

        except Exception as e:
            print(f"Error during widget creation: {e}")

    def select_log_file(self):
        try:
            # Open a file dialog to select a log file
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                # Debugging: Print the selected file path to the console
                print(f"Selected file: {file_path}")
                # Update the label with the selected file path
                self.label.config(text=f"Selected file: {file_path}")
                # Show a message box confirming the file selection
                messagebox.showinfo("File Selected", f"Log file selected: {file_path}")
        except Exception as e:
            print(f"Error during file selection: {e}")

if __name__ == "__main__":
    # Create an instance of the application and run it
    app = LogFileAnalyzerApp()
    app.mainloop()
