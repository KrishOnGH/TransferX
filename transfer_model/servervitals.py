import customtkinter as ctk
import random
import string

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

    def create_widgets(self):
        metrics = [
            ("Clients Connected", 0, 0, "150"),
            ("Active Clients This Week", 0, 1, "45"),
            ("# of Files Stored", 1, 0, "1200"),
            ("Files Stored in Last Month", 1, 1, "350"),
            ("GB Used", 2, 0, "500.75"),
            ("GB Remaining", 2, 1, "199.25")
        ]

        for i, (label, row, col, value) in enumerate(metrics):
            frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
            frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
            
            ctk.CTkLabel(frame, text=label, font=("Arial", 14, "bold")).pack(pady=(10, 5))
            
            var = ctk.StringVar(value=value)
            setattr(self, f"var_{i}", var)
            ctk.CTkLabel(frame, textvariable=var, font=("Arial", 24)).pack(pady=(0, 10))

        last_action_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        last_action_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(last_action_frame, text="Last Action:", font=("Arial", 14, "bold")).pack(pady=(10, 5))
        
        self.last_action_var = ctk.StringVar()
        ctk.CTkLabel(last_action_frame, textvariable=self.last_action_var, wraplength=600, font=("Arial", 12)).pack(padx=10, pady=(0, 10), fill="both", expand=True)

    def update_display(self):
        self.after(1000, self.update_display)

if __name__ == "__main__":
    app = VitalsDisplay()
    app.mainloop()
