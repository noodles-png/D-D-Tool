import customtkinter as ctk
from database.db_manager import DnDDatabase
from utils.helpers import get_modifier, get_prof_bonus, export_character_pdf, get_asset
from tkinter import filedialog


class CharacterTab:
    STATS = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    STAT_VALUES = [str(i) for i in range(1, 21)]

    def __init__(self, parent):
        self.db = DnDDatabase()
        self.current_char_id = None # Initialize current_char_id to save/delete characters
        
        self.left_frame = ctk.CTkFrame(parent)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.right_frame = ctk.CTkFrame(parent)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.editor_tabs = ctk.CTkTabview(self.right_frame)
        self.editor_tabs.pack(fill="both", expand=True)

        self.editor_tabs.add("Overview")
        self.editor_tabs.add("Combat")
        self.editor_tabs.add("Skills")
        self.editor_tabs.add("Spells")
        self.editor_tabs.add("Inventory")

        self.build_basics_tab()
        self.build_combat_tab()
        self.build_character_list()

    def build_character_list(self):
        ctk.CTkButton(
            self.left_frame,
            text="+ New Character",
            command=self.new_character
        ).pack(fill="x", pady=(0, 5))

        self.char_list = ctk.CTkScrollableFrame(self.left_frame, width=200)
        self.char_list.pack(fill="both", expand=True)

        for char in self.db.get_all_characters():
            btn = ctk.CTkButton(
                self.char_list,
                text=char["char_name"],
                command=lambda c=char: self.load_character(c) # Lambda calls load_character only on click
            )
            btn.pack(fill="x", pady=2)

    def build_basics_tab(self):
        self.tab = self.editor_tabs.tab("Overview")
        self.tab.grid_columnconfigure(1, weight=1)
        self.tab.grid_columnconfigure(3, weight=1)
        levels = [str(i) for i in range(1, 21)]

        # Row 1: Name
        ctk.CTkLabel(self.tab, text="Character").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ctk.CTkEntry(self.tab, width=20)
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky="nsew")

        # Row 2: Class & Level
        ctk.CTkLabel(self.tab, text="Class").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        classes = [c["class_name"] for c in self.db.get_all_classes()]
        self.class_entry = ctk.CTkComboBox(self.tab, values=classes, width=20)
        self.class_entry.grid(row=1, column=1, sticky="nsew")
        ctk.CTkLabel(self.tab, text="Level").grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.level_entry = ctk.CTkComboBox(self.tab, values=levels, width=10)
        self.level_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        # Row 3: Race
        ctk.CTkLabel(self.tab, text="Race").grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        races = [r["race_name"] for r in self.db.get_all_races()]
        self.race_entry = ctk.CTkComboBox(self.tab, values=races, width=20)
        self.race_entry.grid(row=2, column=1, columnspan=2, sticky="nsew")

        # Row 4-9: Ability Scores
        self.stats_frame = ctk.CTkFrame(self.tab)
        self.stats_frame.grid(row=4, column=0, columnspan=4, pady=10, sticky="w")

        stats_left = self.STATS[:3]
        stats_right = self.STATS[3:]
        self.stat_entries = {}
        self.mod_labels = {}

        for i, stat in enumerate(stats_left):
            ctk.CTkLabel(self.stats_frame, text=stat).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ctk.CTkComboBox(
                self.stats_frame,
                values=self.STAT_VALUES,
                width=70,
                command=lambda value, s=stat: self.update_modifier(s.lower(), value)
            )
            entry.set("10")
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.stat_entries[stat.lower()] = entry
            mod_label = ctk.CTkLabel(self.stats_frame, text="+0", width=40)
            mod_label.grid(row=i, column=2, padx=5, pady=5)
            self.mod_labels[stat.lower()] = mod_label

        for i, stat in enumerate(stats_right):
            ctk.CTkLabel(self.stats_frame, text=stat).grid(row=i, column=3, padx=5, pady=5, sticky="w")
            entry = ctk.CTkComboBox(
                self.stats_frame,
                values=self.STAT_VALUES,
                width=70,
                command=lambda value, s=stat: self.update_modifier(s.lower(), value)
            )
            entry.set("10")
            entry.grid(row=i, column=4, padx=5, pady=3)
            self.stat_entries[stat.lower()] = entry
            mod_label = ctk.CTkLabel(self.stats_frame, text="+0", width=40)
            mod_label.grid(row=i, column=5, padx=5, pady=5)
            self.mod_labels[stat.lower()] = mod_label

        ctk.CTkButton(self.tab, text="💾 Save", command=self.save_character).grid(
            row=5, column=0, columnspan=4, padx=10, pady=20, sticky="ew"
        )

        ctk.CTkButton(
            self.left_frame,
            text= "DELETE Character",
            fg_color="#cc3333",
            hover_color='#aa2222',
            command=self.delete_character
        ).pack(fill="x", pady=(0,5))

        ctk.CTkButton(self.left_frame,
                      text="Export Character Sheet",
                      command=self.export_pdf
                      ).pack(fill="x", pady=(0,5))

    def update_modifier(self, stat, value):
        mod = get_modifier(value)
        prefix = "+" if mod >= 0 else ""
        self.mod_labels[stat].configure(text=f"{prefix}{mod}")
        if hasattr(self, 'save_labels') and stat in self.save_labels:
            self.update_save(stat)

    def build_combat_tab(self):
        self.tab = self.editor_tabs.tab("Combat")

        ctk.CTkLabel(self.tab, text="Max HP").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.maxhp_entry = ctk.CTkEntry(self.tab, width=20)
        self.maxhp_entry.grid(row=0, column=1, sticky="ew")

        ctk.CTkLabel(self.tab, text="Temp HP").grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.temphp_entry = ctk.CTkEntry(self.tab, width=20)
        self.temphp_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # AC
        ctk.CTkLabel(self.tab, text="AC").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.ac_entry = ctk.CTkEntry(self.tab, width=20)
        self.ac_entry.grid(row=1, column=1, padx=20, sticky="ew")

        # Proficiency bonus
        ctk.CTkLabel(self.tab, text="Proficiency bonus").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.profbonus_entry = ctk.CTkEntry(self.tab, width=20)
        self.profbonus_entry.grid(row=2, column=1, padx=20, sticky="ew")

        # Speed
        ctk.CTkLabel(self.tab, text="Speed").grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.speed_entry = ctk.CTkEntry(self.tab, width=20)
        self.speed_entry.grid(row=3, column=1, padx=20, sticky="ew")

        # Saves
        ctk.CTkLabel(self.tab, text="Saving Throws").grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        self.save_labels = {}
        self.save_checks = {}

        for i, stat in enumerate(self.STATS):
            ctk.CTkLabel(self.tab, text=stat).grid(row=5 + i, column=0, padx=5, pady=5, sticky="ew")

            save_label = ctk.CTkLabel(self.tab, text=get_modifier(self.stat_entries[stat.lower()].get()))
            save_label.grid(row=5 + i, column=1, padx=5, pady=5, sticky="ew")
            self.save_labels[stat.lower()] = save_label

            check_var = ctk.IntVar()
            check = ctk.CTkCheckBox(
                self.tab, text="",
                variable=check_var,
                command=lambda s=stat: self.update_save(s.lower())
            )
            check.grid(row=5 + i, column=2, padx=5, sticky="ew")
            self.save_checks[stat.lower()] = check_var

    def update_save(self, stat):
        mod = get_modifier(self.stat_entries[stat].get())
        if self.save_checks[stat].get() == 1:
            prof = get_prof_bonus(self.level_entry.get())
            total = mod + prof
        else:
            total = mod
        prefix = "+" if total >= 0 else ""
        self.save_labels[stat].configure(text=f"{prefix}{total}")

    def build_skills_tab(self): # TODO Skills mit Prof bonus checkboxen
        pass

    def build_spells_tab(self): # TODO learned spells, spell slots
        pass

    def build_inv_tab(self):    # TODO Inventory & Quantity
        pass


    def load_character(self, char):
        self.current_char = char
        self.current_char_id = char["char_id"]

        # Basic Infos
        self.set_entry(self.name_entry, char["char_name"])
        self.class_entry.set(char["char_class"])
        self.race_entry.set(char["char_race"])
        self.level_entry.set(str(char["char_level"]))

        # Ability scores
        for stat in self.STATS:
            value = char[stat.lower()]
            self.stat_entries[stat.lower()].set(str(value) if value else "10")
            self.update_modifier(stat.lower(), str(value) if value else "10")

        # Combat stats
        self.set_entry(self.maxhp_entry, char["max_hp"])
        self.set_entry(self.ac_entry, char["armor_class"])


    def save_character(self):
        name = self.name_entry.get()
        char_class = self.class_entry.get()
        char_race = self.race_entry.get()
        char_level = int(self.level_entry.get())
        strength = int(self.stat_entries["strength"].get())
        dexterity = int(self.stat_entries["dexterity"].get())
        constitution = int(self.stat_entries["constitution"].get())
        intelligence = int(self.stat_entries["intelligence"].get())
        wisdom = int(self.stat_entries["wisdom"].get())
        charisma = int(self.stat_entries["charisma"].get())
        max_hp = int(self.maxhp_entry.get()) if self.maxhp_entry.get() else None
        armor_class = int(self.ac_entry.get()) if self.ac_entry.get() else None

        self.db.update_character(self.current_char_id,
                                 name,
                                 char_class,
                                 char_race,
                                 char_level,
                                 strength,
                                 dexterity,
                                 constitution,
                                 intelligence,
                                 wisdom,
                                 charisma,
                                 max_hp,
                                 armor_class)

        self.refresh_character_list()

    def delete_character(self):
        if self.current_char_id is not None:
            self.db.delete_character(self.current_char_id)
            self.current_char_id = None
            self.refresh_character_list()

    def set_entry(self, entry, value):
        entry.delete(0, "end")
        entry.insert(0, str(value) if value is not None else "")

    def refresh_character_list(self):
        for widget in self.char_list.winfo_children():
            widget.destroy()
        for char in self.db.get_all_characters():
            btn = ctk.CTkButton(
                self.char_list,
                text=char["char_name"],
                command=lambda c=char: self.load_character(c)
            )
            btn.pack(fill="x", pady=2)

    def new_character(self):
        self.current_char_id = self.db.add_character("New Character", "Fighter", "Human")
        self.refresh_character_list()
        char = self.db.get_character(self.current_char_id)
        self.load_character(char)

    def export_pdf(self):
        if self.current_char_id is None:
            print("No character selected")
            return
        char = self.db.get_character(self.current_char_id)
        print(f"Exporting: {char['char_name']}")

        # Opens save window for the user
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"{char['char_name']}_character_sheet.pdf")

        if path:
            export_character_pdf(get_asset("5E_CharacterSheet_Fillable.pdf"), path, char)


