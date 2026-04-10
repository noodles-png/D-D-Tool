from dice.roller import roll_dice

while True:
    notation = input("Enter your notation: ")
    if notation == "q":
        break
    result = roll_dice(notation)
    print(f"Rolls: {result['rolls']}")
    print(f"Total: {result['total']}")