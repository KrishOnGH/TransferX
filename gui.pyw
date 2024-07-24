import os
import sys
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from process import process_file

def run_process():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        result = process_file(file_path)
        result_label.config(text=result)
    else:
        result_label.config(text="No file path provided.")

# Set up the GUI
app = ctk.CTk()
app.title("TransferX")
app.geometry("400x200")

# Add a button and a result label
button = ctk.CTkButton(app, text="Placeholder Button", command=run_process)
button.pack(pady=20)

result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=20)

# Run the GUI
app.mainloop()
