import json
from database.db_manager import DnDDatabase
from api.dnd_api import DnDApiClient


def sync_all_monsters():
    db = DnDDatabase()
    client = DnDApiClient()
    indices = client.get_all_monsters()
    for i, api_index in enumerate(indices, start=1):
        monster = client.get_monster(api_index)
        monster_name = monster["name"]
        max_hp = monster.get("hit_points")
        monster_size = monster["size"]
        monster_type = monster["type"]
        ac_list = monster.get("armor_class", [])
        armor_class = ac_list[0]["value"] if ac_list else None
        challenge_rating = monster["challenge_rating"]
        raw_json = json.dumps(monster)
        db.add_monster(api_index, monster_name, max_hp, monster_size, monster_type, armor_class, challenge_rating, raw_json)
        print(f"[{i}|{len(indices)}] {monster_name}")
    db.close_connection()

if __name__ == "__main__":
    sync_all_monsters()