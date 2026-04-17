import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("D&D Toolkit")
        self.geometry("900x600")

        logo = CTkImage(
            light_image=Image.open("")
        )




if __name__ == "__main__":
    app = App()
    app.mainloop()