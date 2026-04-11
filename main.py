from dice.roller import roll_dice
from database.db_manager import DnDDatabase


def main():
    while True:
        print("=== D&D Toolkit ===\n")
        print("Choose an option: ")
        print("[1] Character database")
        print("[2] Dice Roller")
        print("[q] Quit")
        menu_choice = input("Choose: ").strip().lower()
        if menu_choice == "q":
            break
        elif menu_choice == "1":
            character_menu()
        elif menu_choice == "2":
            dice_menu()

def character_menu():
    db = DnDDatabase()
    while True:
        print("=== Character database ===")
        print("[1] Add character")
        print("[2] Show all characters")
        print("[3] Update character")
        print("[4] Delete character")
        print("[q] Exit")
        choice = input("Choose: ").strip().lower()
        if choice == "q":
            db.close_connection()
            break
        elif choice == "1":
            char_name = input("Enter character name: ")
            char_class = input("Enter character class: ")
            char_race = input("Enter character race: ")
            db.add_character(char_name, char_class, char_race)
        elif choice == "2":
            print(db.get_all_characters())
        elif choice == "3":
            char_id = input("Enter character ID: ")
            char = db.get_character(char_id)
            if char is None:
                print("No character found")
                continue
            print(f"Current Character: {char_id}")
            print("Press Enter to keep value")

            try:
                new_name = input(f"Name [{char[1]}]: ") or char[1]
                new_class = input(f"Class [{char[2]}]: ") or char[2]
                new_race = input(f"Race [{char[3]}]: ") or char[3]
                new_level = input(f"Level [{char[4]}]: ") or char[4]
                new_hp = input(f"HP [{char[5]}]: ") or char[5]
                new_ac = input(f"AC [{char[6]}]: ") or char[6]
                db.update_character(char_id, new_name, new_class, new_race, new_level, new_hp, new_ac)
            except:
                print("Invalid Input")
                continue
        elif choice == "4":
            char_id = input("Enter char_ID to delete: ")
            choice_validation = input("Are you sure you want to delete this character? (y/n): ").strip().lower()
            if choice_validation == "y":
                db.delete_character(char_id)
            else:
                print("Cancelled")
        else:
            print("Invalid Input")
            continue


def dice_menu():
    while True:
        notation = input("Enter your notation: ")
        if notation == "q":
            break
        try:
            result = roll_dice(notation)
            print(f"Rolls: {result['rolls']}")
            print(f"Total: {result['total']}")
        except ValueError as e:
            print(f"Error: {e}")





if __name__ == "__main__":
    main()