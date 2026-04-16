from database.db_manager import DnDDatabase
from api.dnd_api import DnDApiClient


def sync_all_items():
    db = DnDDatabase()
    client = DnDApiClient()
    indices = client.get_all_items()
    for i, api_index in enumerate(indices, start=1):
        item = client.get_item(api_index)
        item_name = item["name"]
        # item_cost_quant =  # TODO item_cost in db auf zwei segments aufteilen -> besser für Filter/Sortierung
        # item_cost_unit =
        cost = item.get("cost")
        item_cost = f"{cost['quantity']} {cost['unit']}" if cost else None
        item_weight = item.get("weight")
        desc = item.get("desc", [])
        description = "\n\n".join(desc) if desc else None
        db.add_item(api_index, item_name, item_cost, item_weight, description)
        print(f"[{i}|{len(indices)}] {item_name}")
    db.close_connection()


if __name__ == "__main__":
    sync_all_items()
