import tkinter
from peli import Peli


class Kayttoliittyma:

    def __init__(self):
        self.paaikkuna = tkinter.Tk()
        self.alusta_ikkuna()
        self.peli = Peli.palauta_testipeli()

    def alusta_ikkuna(self):
        self.paaikkuna.title("UNO Card Game")
        self.paaikkuna.geometry("1024x768")
        self.paaikkuna.configure(background='grey')

        self.paaikkuna.columnconfigure(0, weight=1)
        self.paaikkuna.columnconfigure(1, weight=1)
        self.paaikkuna.columnconfigure(2, weight=1)
        self.paaikkuna.columnconfigure(3, weight=1)

        self.paaikkuna.rowconfigure(0, weight=1)
        self.paaikkuna.rowconfigure(1, weight=1)
        self.paaikkuna.rowconfigure(2, weight=1)
        self.paaikkuna.rowconfigure(3, weight=1)

    def lataa_kuvat(self):
        pass

    def kaynnista(self):
        self.paaikkuna.mainloop()
        # self.peli.luo_pelaajat()
        # self.peli.pelaa_peli()
