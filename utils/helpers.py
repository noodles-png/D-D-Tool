import os
import customtkinter as ctk
from pypdf import PdfReader, PdfWriter


def get_asset(filename):
    return os.path.join(os.path.dirname(__file__), "..", "assets", filename)


def get_modifier(value):
    """ Returns the calculated modifier based on the ability score """
    value = int(value)
    modifier = round((value - 10) // 2)
    return modifier


def _mod_str(value):
    """ Returns the modifier string based on the ability score """
    mod = get_modifier(value)
    return f"+{mod}" if mod >= 0 else str(mod)


def get_prof_bonus(level):
    """ Returns the proficiency bonus based on character level """
    return (int(level) - 1) // 4 + 2


def get_spell_dc(prof_bonus, stat_modifier):
    """ Returns the spell difficulty check
     Args:
         prof_bonus: proficiency bonus calculated from get_prof_bonus
         stat_modifier: Ability score modifier calculated from get_modifier
     Returns:
         spell_dc: integer
     """
    spell_dc = 8 + prof_bonus + stat_modifier
    return spell_dc


class CollapsibleSection:
    """ """
    def __init__(self, parent, title):
        self.title = title
        self.is_open = False

        self.header_btn = ctk.CTkButton(parent, text=f"▶ {title}", command=self.toggle_button, fg_color="#222222")
        self.header_btn.pack(fill="x", pady=2)

        self.content = ctk.CTkFrame(parent)

    def toggle_button(self):
        self.is_open = not self.is_open

        if self.is_open:
            self.content.pack(fill="x", after=self.header_btn)
            self.header_btn.configure(text=f"▼ {self.title}")
        else:
            self.content.pack_forget()
            self.header_btn.configure(text=f"▶ {self.title}")


def export_character_pdf(template_path, output_path, char_data):
    """ Creates a character sheet in PDF format"""
    reader = PdfReader(template_path)
    writer = PdfWriter()
    writer.append(reader)

    fields = {
        "CharacterName": char_data["char_name"],
        "ClassLevel": f"{char_data['char_class']} {char_data['char_level']}",
        "Race ": char_data["char_race"],
        "STR": str(char_data["strength"]),
        "DEX": str(char_data["dexterity"]),
        "CON": str(char_data["constitution"]),
        "INT": str(char_data["intelligence"]),
        "WIS": str(char_data["wisdom"]),
        "CHA": str(char_data["charisma"]),
        "STRmod": _mod_str(char_data["strength"]),
        "DEXmod ": _mod_str(char_data["dexterity"]),
        "CONmod": _mod_str(char_data["constitution"]),
        "INTmod": _mod_str(char_data["intelligence"]),
        "WISmod": _mod_str(char_data["wisdom"]),
        "CHamod": _mod_str(char_data["charisma"]),
        "HPMax": str(char_data["max_hp"] or ""),
        "AC": str(char_data["armor_class"] or ""),
        "ProfBonus": str(get_prof_bonus(char_data["char_level"])),
        "Speed": str(char_data["speed"] if char_data["speed"] else "30"),
    }

    writer.update_page_form_field_values(writer.pages[0], fields)

    with open(output_path, "wb") as f:
        writer.write(f)








