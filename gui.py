import os
import sys
import random
import customtkinter as ctk
from transfer_model.sender import send_file, SERVER_PORT, IP
from transfer_model.receiver import receive_file

def run_process():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

        if os.path.isfile(file_path):
            UUID = random.randint(100000, 999999)
            status = send_file({"IP": IP, "Port": SERVER_PORT}, UUID, file_path)

            if status['message'] == "error":
                result_label.configure(text="Error")
            else:
                result_label.configure(text=f"UUID: {UUID}")

        elif os.path.isdir(file_path):
            add_uuid_input()
    
        else:
            file_selected_label.configure(text="The provided path is neither a file nor a folder.")

def add_uuid_input():
    uuid_label.pack(pady=10)
    uuid_entry.pack(pady=10)
    receive_button.pack(pady=10)

def receive_process():
    file_path = sys.argv[1]
    UUID = uuid_entry.get()
    status = receive_file({"IP": IP, "Port": SERVER_PORT}, UUID, file_path)

    if status['message'] == 'error':
        uuid_label.pack_forget()
        uuid_entry.pack_forget()
        receive_button.pack_forget()
        result_label.configure(text=f"{status['details']}")
    else:
        result_label.configure(text="Success")

# Set up the GUI
app = ctk.CTk()
app.title("TransferX")
app.geometry("400x300")

header = ctk.CTkLabel(app, text="TransferX")
header.pack(pady=10)

file_selected_label = ctk.CTkLabel(app, text="Nothing selected")
file_selected_label.pack(pady=10)

button = ctk.CTkButton(app, text="Continue", command=run_process)
button.pack(pady=20)

result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=20)

uuid_label = ctk.CTkLabel(app, text="Receive File - Enter UUID:")
uuid_entry = ctk.CTkEntry(app, placeholder_text="Enter UUID")
receive_button = ctk.CTkButton(app, text="Receive", command=receive_process)

# Update labels
if len(sys.argv) > 1:
    file_path = sys.argv[1]

    if os.path.isfile(file_path):
        header.configure(text="Send File")
        file_selected_label.configure(text=f"{os.path.basename(file_path)} is selected")

    elif os.path.isdir(file_path):
        header.configure(text="Receive File")
        file_selected_label.configure(text=f"{os.path.basename(file_path)} is selected")

    else:
        file_selected_label.configure(text="The provided path is neither a file nor a folder.")

else:
    file_selected_label.configure(text="No path provided.")

# Run the GUI
app.mainloop()