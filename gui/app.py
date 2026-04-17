from logging import setLogRecordFactory
from dice.roller import roll_dice
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from utils.helpers import get_asset


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("Logo-darkbg.ico")
        self.title("D&D Toolkit")
        self.geometry("900x600")

        # Logo
        logo = CTkImage(
            light_image=Image.open("Logo-darkbg.png"),
            dark_image=Image.open("Logo-transparent.png"),
            size=(40,40)
        )

        # Tab Navigation
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        # Added Tabs
        self.tabs.add("Characters")
        self.tabs.add("Spells")
        self.tabs.add("Monsters")
        self.tabs.add("Dice Roller")

        DiceTab(self.tabs.tab("Dice Roller"))

class DiceTab:
    def __init__(self, parent):
        """ Defines the structure of the dice roller tab """
       # ctk.CTkLabel(parent, text="Dice Roller").grid(row=0, column=0)
       # self.entry = ctk.CTkEntry(parent)
        #self.entry.grid(row=0, column=1)

        # Dice Buttons - Icon Images
        d2_icon = ctk.CTkImage(light_image=Image.open(get_asset("d2.png")), size=(200,200))
        d4_icon = ctk.CTkImage(light_image=Image.open(get_asset("d4.png")), size=(200,200))
        d6_icon = ctk.CTkImage(light_image=Image.open(get_asset("d6.png")), size=(200,200))
        d8_icon = ctk.CTkImage(light_image=Image.open(get_asset("d8.png")), size=(200,200))
        d10_icon = ctk.CTkImage(light_image=Image.open(get_asset("d10.png")), size=(200,200))
        d12_icon = ctk.CTkImage(light_image=Image.open(get_asset("d12.png")), size=(200,200))
        d20_icon = ctk.CTkImage(light_image=Image.open(get_asset("d20.png")), size=(200,200))
        d100_icon = ctk.CTkImage(light_image=Image.open(get_asset("d100.png")), size=(200,200))

        # Dice Buttons - Settings
        d2_button = ctk.CTkButton(parent, text="", image=d2_icon, width=200, height=200, fg_color="transparent")
        d2_button.grid(row=1, column=0)
        d4_button = ctk.CTkButton(parent, text="", image=d4_icon, width=200, height=200, fg_color="transparent")
        d4_button.grid(row=1, column=1)
        d6_button = ctk.CTkButton(parent, text="", image=d6_icon, width=200, height=200, fg_color="transparent")
        d6_button.grid(row=1, column=2)
        d8_button = ctk.CTkButton(parent, text="", image=d8_icon, width=200, height=200, fg_color="transparent")
        d8_button.grid(row=1, column=3)
        d10_button = ctk.CTkButton(parent, text="", image=d10_icon, width=200, height=200, fg_color="transparent")
        d10_button.grid(row=2, column=0)
        d12_button = ctk.CTkButton(parent, text="", image=d12_icon, width=200, height=200, fg_color="transparent")
        d12_button.grid(row=2, column=1)
        d20_button = ctk.CTkButton(parent, text="", image=d20_icon, width=200, height=200, fg_color="transparent")
        d20_button.grid(row=2, column=2)
        d100_button = ctk.CTkButton(parent, text="", image=d100_icon, width=200, height=200, fg_color="transparent")
        d100_button.grid(row=2, column=3)




if __name__ == "__main__":
    app = App()
    app.mainloop()