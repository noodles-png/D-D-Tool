import customtkinter as ctk
from database.db_manager import DnDDatabase

class CharacterTab:
    def __init__(self, parent):
        self.db = DnDDatabase()
        
        self.left_frame = ctk.CTkFrame(parent)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.right_frame = ctk.CTkFrame(parent)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.build_character_list()
        self.build_editor()

    def build_character_list(self):
        self.char_list = ctk.CTkScrollableFrame(self.left_frame, width=200)
        self.char_list.pack(fill="both", expand=True)

        for char in self.db.get_all_characters():
            btn = ctk.CTkButton(
                self.char_list,
                text=char["char_name"],
                command=lambda c=char: self.load_character(c)
            )
            btn.pack(fill="x", pady=2)

    def build_editor(self):
        self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(3, weight=1)
        levels = [str(i) for i in range(1, 21)]

        # Row 1: Name
        ctk.CTkLabel(self.right_frame, text="Character").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ctk.CTkEntry(self.right_frame, width=20)
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky="nsew")

        # Row 2: Class & Level
        ctk.CTkLabel(self.right_frame, text="Class").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        classes =[c["class_name"] for c in self.db.get_all_classes()]
        self.class_entry = ctk.CTkComboBox(self.right_frame, values=classes, width=20)
        self.class_entry.grid(row=1, column=1, sticky="nsew")
        ctk.CTkLabel(self.right_frame, text="Level").grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.level_entry = ctk.CTkComboBox(self.right_frame, values=levels, width=10)
        self.level_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)


        # Row 3: Race
        ctk.CTkLabel(self.right_frame, text="Race").grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        races = [r["race_name"] for r in self.db.get_all_races()]
        self.race_entry = ctk.CTkComboBox(self.right_frame, values=races, width=20)
        self.race_entry.grid(row=2, column=1, columnspan=2, sticky="nsew")

        # Row 4-9: Ability Scores
        self.stats_frame = ctk.CTkFrame(self.right_frame)
        self.stats_frame.grid(row=4, column=0, columnspan=4, pady=10, sticky="w")

        stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        self.stat_entries = {}

        for i, stat in enumerate(stats):
            ctk.CTkLabel(self.stats_frame, text=stat). grid(row=i, column=0, padx=5, pady=3, sticky="w")
            entry = ctk.CTkComboBox(self.stats_frame, values=levels, width=70)
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.stat_entries[stat.lower()] = entry

    def load_character(self):
        print(f"Chosen: {char['char_name']}")   # Placeholder

