import requests

class DnDApiClient:
    BASE_URL = "https://www.dnd5eapi.co/api/2014"

    def get_all_spells(self):
        response = requests.get(f"{self.BASE_URL}/spells")
        data = response.json()
        return [item["index"] for item in data["results"]]

    def get_spell(self, spell_choice):
        response = requests.get(f"{self.BASE_URL}/spells/{spell_choice}")
        return response.json()

    def get_all_items(self):
        response = requests.get(f"{self.BASE_URL}/2014/equipment")
        data = response.json()
        return [item["index"] for item in data["results"]]

    def get_item(self, item_choice):
        response = requests.get(f"{self.BASE_URL}/equipment/{item_choice}")
        return response.json()


if __name__ == '__main__':
    indices = get_all_spells()
    print(f"Gefunden: {len(indices)} Zauber")
    print(indices[:5])