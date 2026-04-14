from database.db_manager import DnDDatabase
from api.dnd_api import get_all_spells, get_spell


def sync_all_spells():
    db = DnDDatabase()
    indices = get_all_spells()
    for i, api_index in enumerate(indices, start=1):
        spell = get_spell(api_index)
        spell_name = spell["name"]
        spell_level = spell["level"]
        spell_school = spell["school"]["name"]
        description = "\n\n".join(spell["desc"])
        db.add_spell(api_index, spell_name, spell_level, spell_school, description)
        print(f"[{i}|{len(indices)}] {spell_name}")
    db.close_connection()

if __name__ == "__main__":
    sync_all_spells()