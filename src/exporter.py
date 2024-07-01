import pandas as pd
from tkinter import filedialog, messagebox

def export_to_excel(info_list, title):
    df = pd.DataFrame(info_list, columns=["Attribute", "Value"])
    output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if output_path:
        df.to_excel(output_path, index=False)
        messagebox.showinfo("Export Complete", f"Data exported to {output_path}")
