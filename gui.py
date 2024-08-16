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

            file_selected_label.destroy()
            button.destroy()           
            header.place(relx=0.5, rely=0.475, anchor='center')
            result_label.place(relx=0.5, rely=0.525, anchor='center')     

            if status['message'] == "error":
                result_label.configure(text="Error")
            else:
                result_label.configure(text=f"UUID: {UUID}")

        elif os.path.isdir(file_path):
            header.place(relx=0.5, rely=0.4, anchor='center')
            file_selected_label.destroy()
            button.destroy()

            add_uuid_input()

        else:
            file_selected_label.configure(text="The provided path is neither a file nor a folder.")

def add_uuid_input():
    uuid_label.place(relx=0.5, rely=0.4, anchor='center', y=30)
    uuid_entry.place(relx=0.5, rely=0.4, anchor='center', y=60)
    receive_button.place(relx=0.5, rely=0.4, anchor='center', y=90)

def receive_process():
    file_path = sys.argv[1]
    UUID = uuid_entry.get()
    status = receive_file({"IP": IP, "Port": SERVER_PORT}, UUID, file_path)

    uuid_label.destroy()
    uuid_entry.destroy()
    receive_button.destroy()
    header.place(relx=0.5, rely=0.475, anchor='center')
    result_label.place(relx=0.5, rely=0.525, anchor='center')
    
    if status['message'] == 'error':
        result_label.configure(text=f"{status['details']}")
    else:
        result_label.configure(text="Success")

# Set up the GUI
app = ctk.CTk()
app.title("TransferX")
app.after(0, lambda: app.state('zoomed'))

header_font = ("Arial", 24, "bold")
default_font = ("Arial", 16)

header = ctk.CTkLabel(app, text="TransferX", font=header_font)
header.place(relx=0.5, rely=0.4, anchor='center')

file_selected_label = ctk.CTkLabel(app, text="Nothing selected", font=default_font)
file_selected_label.place(relx=0.5, rely=0.45, anchor='center')

button = ctk.CTkButton(app, text="Continue", command=run_process)
button.place(relx=0.5, rely=0.5, anchor='center')

result_label = ctk.CTkLabel(app, text="", font=default_font)
result_label.place(relx=0.5, rely=0.55, anchor='center')

uuid_label = ctk.CTkLabel(app, text="Receive File - Enter UUID:", font=default_font)
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
