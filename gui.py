import os
import sys
import random
import customtkinter as ctk
from transfer_model.sender import send_file, SERVER_PORT, IP
from transfer_model.receiver import receive_file
from PIL import Image, ImageTk

def run_process():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

        if os.path.isfile(file_path):
            UUID = random.randint(100000, 999999)
            is_permanent_value = "True" if is_permanent_var.get() else "False"
            status = send_file({"IP": IP, "Port": SERVER_PORT}, UUID, file_path, is_permanent_value)

            file_selected_label.destroy()
            button.destroy()           
            is_permanent_checkbox.destroy()
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
    if len(UUID) == 0:
        return
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

is_permanent_var = ctk.BooleanVar(value=False)
is_permanent_checkbox = ctk.CTkCheckBox(app, text="Is Permanent", variable=is_permanent_var, font=default_font)
is_permanent_checkbox.place(relx=0.5, rely=0.5, anchor='center')

button = ctk.CTkButton(app, text="Continue", command=run_process)
button.place(relx=0.5, rely=0.55, anchor='center')

result_label = ctk.CTkLabel(app, text="", font=default_font)
result_label.place(relx=0.5, rely=0.55, anchor='center')

uuid_label = ctk.CTkLabel(app, text="Receive File - Enter UUID:", font=default_font)
uuid_entry = ctk.CTkEntry(app, placeholder_text="Enter UUID")
receive_button = ctk.CTkButton(app, text="Receive", command=receive_process)

settings_icon_path = os.path.join(os.path.dirname(__file__), "icons", "settings.png")
settings_icon_image = ImageTk.PhotoImage(Image.open(settings_icon_path).resize((30, 30)))
settings_label = ctk.CTkLabel(app, image=settings_icon_image, text="")
settings_label.place(x=10, y=10)

def on_settings_click(event):
    settings_label.place_forget()

    settings_screen = ctk.CTkFrame(app, width=app.winfo_width(), height=app.winfo_height())
    settings_screen.place(x=0, y=0)

    settings_screen_label = ctk.CTkLabel(settings_screen, text="Settings", font=("Arial", 24, "bold"))
    settings_screen_label.place(relx=0.5, y=15, anchor="n")

    x_icon_path = os.path.join(os.path.dirname(__file__), "icons", "close.png")
    x_icon_image = ImageTk.PhotoImage(Image.open(x_icon_path).resize((25, 25)))

    x_label = ctk.CTkLabel(settings_screen, image=x_icon_image, text="")
    x_label.place(relx=1.0, x=-40, y=12, anchor="ne")

    # Server IP input
    server_ip_label = ctk.CTkLabel(settings_screen, text="Server IP:", font=("Arial", 16))
    server_ip_label.place(relx=0.5, y=60, anchor="center")

    server_ip_entry = ctk.CTkEntry(settings_screen, placeholder_text="Enter Server IP")
    server_ip_entry.place(relx=0.5, y=90, anchor="center")

    save_ip_button = ctk.CTkButton(settings_screen, text="Save", command=lambda: save_ip(server_ip_entry.get()))
    save_ip_button.place(relx=0.5, y=130, anchor="center")

    # Server Port input
    server_port_label = ctk.CTkLabel(settings_screen, text="Server Port:", font=("Arial", 16))
    server_port_label.place(relx=0.5, y=170, anchor="center")

    server_port_entry = ctk.CTkEntry(settings_screen, placeholder_text="Enter Server Port")
    server_port_entry.place(relx=0.5, y=200, anchor="center")

    save_port_button = ctk.CTkButton(settings_screen, text="Save", command=lambda: save_port(server_port_entry.get()))
    save_port_button.place(relx=0.5, y=240, anchor="center")

    def save_ip(ip):
        print(f"Server IP: {ip}")
        # Add code to handle saving the IP value

    def save_port(port):
        print(f"Server Port: {port}")

    def close_settings_screen(event):
        settings_screen.destroy()
        settings_label.place(x=10, y=10)

    x_label.bind("<Button-1>", close_settings_screen)

    x_label.bind("<Enter>", lambda e: x_label.configure(cursor="hand2"))
    x_label.bind("<Leave>", lambda e: x_label.configure(cursor=""))

settings_label.bind("<Button-1>", on_settings_click)

settings_label.bind("<Enter>", lambda e: settings_label.configure(cursor="hand2"))
settings_label.bind("<Leave>", lambda e: settings_label.configure(cursor=""))

# Update labels
if len(sys.argv) > 1:
    file_path = sys.argv[1]

    if os.path.isfile(file_path):
        header.configure(text="Send File")
        file_selected_label.configure(text=f"{os.path.basename(file_path)} is selected")

    elif os.path.isdir(file_path):
        is_permanent_checkbox.destroy()
        button.place(relx=0.5, rely=0.5, anchor='center')
        header.configure(text="Receive File")
        file_selected_label.configure(text=f"{os.path.basename(file_path)} is selected")

    else:
        file_selected_label.configure(text="The provided path is neither a file nor a folder.")

else:
    file_selected_label.configure(text="No path provided.")

# Run the GUI
app.mainloop()
