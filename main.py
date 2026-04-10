from dice.roller import roll_dice
from database.db_manager import DnDDatabase

"""
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
"""


def main():
    db = DnDDatabase()

    while True:
        print("=== D&D Toolkit ===")
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
            pass
        elif choice == "4":
            char_id = input("Enter character name to delete: ")
            choice_validation = input("Are you sure you want to delete this character? (y/n): ").strip().lower()
            if choice_validation == "y":
                db.delete_character(char_id)
            else:
                print("Cancelled")



if __name__ == "__main__":
    main()