import customtkinter as ctk
from server import TEMP_FOLDER, SERVER_DATA_FILE, UUIDS_FILE
import os
import datetime
from dateutil import parser
import shutil
import json

class VitalsDisplay(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("System Vitals")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.main_frame.columnconfigure((0, 1), weight=1)
        self.main_frame.rowconfigure((0, 1, 2, 3), weight=1)

        self.create_widgets()

        self.update_display()

    def get_data(self):
        if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), SERVER_DATA_FILE)):
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), SERVER_DATA_FILE), 'r') as f:
                server_data = json.load(f)
        else:
            server_data = {"Clients": {}}

        clients = server_data['Clients']
        numClients = len(clients)
        numActiveClients = 0

        for clientSignature in clients:
            client = clients[clientSignature]
            if datetime.date.today() - parser.parse(client["Last Date Active"]).date() <= datetime.timedelta(days=7):
                numActiveClients += 1

        if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), UUIDS_FILE)):
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), UUIDS_FILE), 'r') as f:
                UUIDS = json.load(f)
        else:
            UUIDS = {}

        numFiles = len(UUIDS)
        numRecentFiles = 0

        for uuid in UUIDS:
            date_stored = UUIDS[uuid]['Date']
            if datetime.date.today() - parser.parse(date_stored).date() <= datetime.timedelta(days=30):
                numRecentFiles += 1

        total, used, free = shutil.disk_usage(os.path.join(os.path.dirname(os.path.abspath(__file__)), TEMP_FOLDER))

        used = used / (1024 ** 3)
        free = free / (1024 ** 3)
        
        return {"Clients Connected": numClients, "Active Clients": numActiveClients, "Files Stored": numFiles, "Recent Files": numRecentFiles, "GB Used": used, "GB Remaining": free}

    def create_widgets(self):
        data = self.get_data()

        metrics = [
            ("Clients Connected", 0, 0, data['Clients Connected']),
            ("Active Clients", 0, 1, data['Active Clients']),
            ("Files Stored", 1, 0, data['Files Stored']),
            ("Recent Files", 1, 1, data['Recent Files']),
            ("GB Used", 2, 0, data['GB Used']),
            ("GB Remaining", 2, 1, data['GB Remaining'])
        ]

        self.vars = {}
        for i, (label, row, col, value) in enumerate(metrics):
            frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
            frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
            
            ctk.CTkLabel(frame, text=label, font=("Arial", 14, "bold")).pack(pady=(10, 5))
            
            var = ctk.StringVar(value=value)
            self.vars[label] = var
            ctk.CTkLabel(frame, textvariable=var, font=("Arial", 24)).pack(pady=(0, 10))

    def update_display(self):
        data = self.get_data()

        for label in self.vars.keys():
            if label in data:
                self.vars[label].set(data[label])

        self.after(1000, self.update_display)

if __name__ == "__main__":
    app = VitalsDisplay()
    app.mainloop()
