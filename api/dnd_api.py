import requests




def get_spell(spell_choice):
    response = requests.get(f"https://www.dnd5eapi.co/api/2014/spells/{spell_choice}")
    return response.json()








if __name__ == '__main__':
    spell_choice = input("Enter a spell choice: ")
    spell = get_spell(spell_choice)
    print(spell)