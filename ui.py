import tkinter as tk
from peli import Peli
from config import Config


class UnoCardGame(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1024x768+8+100")

        paaikkuna = tk.Frame(self)
        paaikkuna.grid(row=0, column=0, sticky="nsew")

        paaikkuna.rowconfigure(0, weight=1)
        paaikkuna.columnconfigure(0, weight=1)

        self.framet = {}

        for F in (Aloitusframe, Peliframe):
            frame = F(paaikkuna, self)
            self.framet[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.nayta_frame(Aloitusframe)

    def nayta_frame(self, frame):
        frame1 = self.framet[frame]
        frame1.tkraise()


class Aloitusframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Aloitusframe")
        label.grid(row=0, column=0, columnspan=2)

        nappi = tk.Button(self, text="Peliframeen",
                          command=lambda: controller.nayta_frame(Peliframe))
        nappi.grid(row=1, column=0)

        nappi2 = tk.Button(self, text="Lopeta",
                           command=lambda: controller.quit())
        nappi2.grid(row=1, column=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


class Peliframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Peliframe")
        label.grid(row=0, column=0, columnspan=2)

        nappi = tk.Button(self, text="Aloitusframeen",
                          command=lambda: controller.nayta_frame(Aloitusframe))
        nappi.grid(row=1, column=0)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
