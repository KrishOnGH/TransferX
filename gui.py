import os
import sys
import json
import socket
import random
import customtkinter as ctk
from PIL import Image, ImageTk
from transfer_model.sender import send_file
from transfer_model.receiver import receive_file

preferences_file = os.path.join(os.path.dirname(__file__), 'preferences.json')
default_preferences = {'Server IP': 'myowncloudserver.com', 'Server Port': 443, 'Encryption Key': 91827}

def loadPreferences():
    if os.path.exists(preferences_file):
        with open(preferences_file, 'r') as file:
            preferences = json.load(file)
            if not "Server IP" in preferences or not "Server Port" in preferences or not "Encryption Key" in preferences:
                preferences = default_preferences
    else:
        preferences = default_preferences

    with open(preferences_file, 'w') as file:
        json.dump(preferences, file, indent=4)
    
    return preferences

preferences = loadPreferences()

IP = preferences['Server IP']
SERVER_PORT = int(preferences['Server Port'])
ENCRYPTION_KEY = int(preferences['Encryption Key'])

def setPreference(prefKey, prefValue):
    if os.path.exists(preferences_file):
        with open(preferences_file, 'r') as file:
            preferences = json.load(file)
            if not "Server IP" in preferences or not "Server Port" in preferences or not "Encryption Key" in preferences:
                preferences = default_preferences
    else:
        preferences = default_preferences

    preferences[prefKey] = prefValue

    with open(preferences_file, 'w') as file:
        json.dump(preferences, file, indent=4)

def run_process():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

        if os.path.isfile(file_path):
            preferences = loadPreferences()
            IP = preferences['Server IP']
            SERVER_PORT = int(preferences['Server Port'])       
            ENCRYPTION_KEY = int(preferences['Encryption Key'])

            file_selected_label.destroy()
            button.destroy()
            is_permanent_checkbox.destroy()
            header.place(relx=0.5, rely=0.475, anchor='center')
            result_label.place(relx=0.5, rely=0.525, anchor='center')     

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect((IP, SERVER_PORT))
                except:
                    result_label.configure(text=f"Incorrect Server (Change in settings)")
                    return

                s.sendall(b'checker')

                answer = s.recv(4096).decode()

                if answer != 'TransferX Server ACK':
                    result_label.configure(text=f"Incorrect Server (Change in settings)")
                    return

            UUID = random.randint(100000, 999999)
            is_permanent_value = "True" if is_permanent_var.get() else "False"
            status = send_file({"IP": IP, "Port": SERVER_PORT}, UUID, file_path, is_permanent_value, ENCRYPTION_KEY)

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

    preferences = loadPreferences()
    IP = preferences['Server IP']
    SERVER_PORT = int(preferences['Server Port'])
    ENCRYPTION_KEY = int(preferences['Encryption Key'])

    uuid_label.destroy()
    uuid_entry.destroy()
    receive_button.destroy()
    header.place(relx=0.5, rely=0.475, anchor='center')
    result_label.place(relx=0.5, rely=0.525, anchor='center')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((IP, SERVER_PORT))
        except:
            result_label.configure(text=f"Incorrect Server (Change in settings)")
            return

        s.sendall(b'checker')

        answer = s.recv(4096).decode()

        if answer != 'TransferX Server ACK':
            print(answer)
            result_label.configure(text=f"Incorrect Server (Change in settings)")
            return

    status = receive_file({"IP": IP, "Port": SERVER_PORT}, UUID, file_path, ENCRYPTION_KEY)

    if status['message'] == 'error':
        result_label.configure(text=f"{status['details']}")
    else:
        result_label.configure(text="Success")

# Set up the GUI
app = ctk.CTk()
app.title("TransferX")
app.after(0, lambda: app.state('zoomed'))

icon_path = os.path.join(os.path.dirname(__file__), "icons", "settings.png")
try:
    icon = Image.open(icon_path)
    icon = ImageTk.PhotoImage(icon)
    app.iconphoto(False, icon)
except Exception as e:
    print(f"Failed to load icon: {e}")

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
settings_label.place(relx=0, x=40, y=12, anchor="ne")

def settings_screen(event):
    preferences = loadPreferences()
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

    server_ip_entry = ctk.CTkEntry(settings_screen)
    IP = preferences['Server IP']
    server_ip_entry.insert(0, IP)
    server_ip_entry.place(relx=0.5, y=90, anchor="center")

    save_ip_button = ctk.CTkButton(settings_screen, text="Save", command=lambda: save_ip(server_ip_entry.get()))
    save_ip_button.place(relx=0.5, y=130, anchor="center")

    # Server Port input
    server_port_label = ctk.CTkLabel(settings_screen, text="Server Port:", font=("Arial", 16))
    server_port_label.place(relx=0.5, y=170, anchor="center")

    server_port_entry = ctk.CTkEntry(settings_screen)
    SERVER_PORT = int(preferences['Server Port'])
    server_port_entry.insert(0, str(SERVER_PORT))   
    server_port_entry.place(relx=0.5, y=200, anchor="center")

    save_port_button = ctk.CTkButton(settings_screen, text="Save", command=lambda: save_port(server_port_entry.get()))
    save_port_button.place(relx=0.5, y=240, anchor="center")

    # Encryption Key input
    encryption_key_label = ctk.CTkLabel(settings_screen, text="Encryption Key:", font=("Arial", 16))
    encryption_key_label.place(relx=0.5, y=280, anchor="center")

    encryption_key_entry = ctk.CTkEntry(settings_screen)
    ENCRYPTION_KEY = int(preferences['Encryption Key'])
    encryption_key_entry.insert(0, str(ENCRYPTION_KEY))   
    encryption_key_entry.place(relx=0.5, y=310, anchor="center")

    save_key_button = ctk.CTkButton(settings_screen, text="Save", command=lambda: save_key(encryption_key_entry.get()))
    save_key_button.place(relx=0.5, y=350, anchor="center")

    def save_ip(ip):
        setPreference(f"Server IP", ip)

    def save_port(port):
        setPreference("Server Port", port)    

    def save_key(key):
        setPreference("Encryption Key", key)

    def close_settings_screen(event):
        settings_screen.destroy()
        settings_label.place(relx=0, x=40, y=12, anchor="ne")

    x_label.bind("<Button-1>", close_settings_screen)

    x_label.bind("<Enter>", lambda e: x_label.configure(cursor="hand2"))
    x_label.bind("<Leave>", lambda e: x_label.configure(cursor=""))

settings_label.bind("<Button-1>", settings_screen)

settings_label.bind("<Enter>", lambda e: settings_label.configure(cursor="hand2"))
settings_label.bind("<Leave>", lambda e: settings_label.configure(cursor=""))

database_icon_path = os.path.join(os.path.dirname(__file__), "icons", "database.png")
database_icon_image = ImageTk.PhotoImage(Image.open(database_icon_path).resize((30, 30)))
database_label = ctk.CTkLabel(app, image=database_icon_image, text="")
database_label.place(relx=1.0, x=-40, y=12, anchor="ne")

def database_screen(event):
    database_label.place_forget()

    database_screen = ctk.CTkFrame(app, width=app.winfo_width(), height=app.winfo_height())
    database_screen.place(x=0, y=0)

    scrollable_frame = ctk.CTkScrollableFrame(database_screen, width=app.winfo_width(), height=app.winfo_height() - 80, fg_color="transparent")
    scrollable_frame.place(x=0, y=60)

    preferences = loadPreferences()
    IP = preferences['Server IP']
    SERVER_PORT = int(preferences['Server Port'])
    canConnect = True

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((IP, SERVER_PORT))
            s.sendall(b'checker')

            answer = s.recv(4096).decode()

            if answer != 'TransferX Server ACK':
                result = ctk.CTkLabel(database_screen, text="Incorrect Server (Change in settings)", font=("Arial", 16))
                result.place(relx=0.5, y=80, anchor="n")
                canConnect = False

        except:
            canConnect = False
            result = ctk.CTkLabel(database_screen, text="Incorrect Server (Change in settings)", font=("Arial", 16))
            result.place(relx=0.5, y=80, anchor="n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            if canConnect:
                s.connect((IP, SERVER_PORT))
                s.sendall(b'dbdataquery')

                dbData = json.loads(s.recv(1024).decode())
                for key, value in dbData.items():
                    frame_width = min(int(app.winfo_width() * 0.45), 600)
                    frame = ctk.CTkFrame(scrollable_frame, corner_radius=10, border_width=2, width=frame_width, height=120)
                    frame.pack_propagate(False)
                    frame.pack(pady=10, anchor="center")

                    filename = value["Filename"][:-8] if len(value["Filename"]) > 8 else value["Filename"]

                    filename_label = ctk.CTkLabel(frame, text=filename, 
                                                font=("Arial", 16),
                                                anchor="w")
                    filename_label.place(x=10, y=10)

                    delete_icon_path = os.path.join(os.path.dirname(__file__), "icons", "delete.png")
                    delete_icon_image = ImageTk.PhotoImage(Image.open(delete_icon_path).resize((30, 30)))

                    delete_label = ctk.CTkLabel(frame, image=delete_icon_image, text="")
                    delete_label.place(relx=1.0, x=-30, y=10, anchor="ne")

                    uuid_label = ctk.CTkLabel(frame, text=f"UUID: {key}", 
                                            font=("Arial", 12),
                                            anchor="w")
                    uuid_label.place(x=10, y=40)

                    permanent_label = ctk.CTkLabel(frame, text=f"Permanent: {value['Permanent']}", 
                                                font=("Arial", 12),
                                                anchor="w")
                    permanent_label.place(x=10, y=60)

                    def delete(event, key=key, frame=frame):
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((IP, SERVER_PORT))
                            s.sendall(b'delete')
                            s.recv(1024)
                            s.sendall(str(key).encode())
                            frame.destroy()

                    delete_label.bind("<Button-1>", delete)

                    delete_label.bind("<Enter>", lambda e, label=delete_label: label.configure(cursor="hand2"))
                    delete_label.bind("<Leave>", lambda e, label=delete_label: label.configure(cursor=""))

        except KeyError as e:
            pass

    database_screen_label = ctk.CTkLabel(database_screen, text="Database", font=("Arial", 24, "bold"))
    database_screen_label.place(relx=0.5, y=20, anchor="n")

    x_icon_path = os.path.join(os.path.dirname(__file__), "icons", "close.png")
    x_icon_image = ImageTk.PhotoImage(Image.open(x_icon_path).resize((25, 25)))

    x_label = ctk.CTkLabel(database_screen, image=x_icon_image, text="")
    x_label.place(relx=1.0, x=-40, y=12, anchor="ne")

    def close_database_screen(event):
        database_screen.destroy()
        database_label.place(relx=1.0, x=-40, y=12, anchor="ne")    

    x_label.bind("<Button-1>", close_database_screen)

    x_label.bind("<Enter>", lambda e: x_label.configure(cursor="hand2"))
    x_label.bind("<Leave>", lambda e: x_label.configure(cursor=""))

database_label.bind("<Button-1>", database_screen)

database_label.bind("<Enter>", lambda e: database_label.configure(cursor="hand2"))
database_label.bind("<Leave>", lambda e: database_label.configure(cursor=""))

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
