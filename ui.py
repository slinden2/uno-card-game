import tkinter as tk
from tkinter import ttk
from peli import Peli
from config import Config


class UnoCardGame(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.geometry("1024x768+16+100")
        self.configure(background="green")

        tk.Tk.wm_title(self, "UNO Card Game")

        paaikkuna = tk.Frame(self)
        paaikkuna.pack(side="top", fill="both", expand=True)

        paaikkuna.rowconfigure(0, weight=1)
        paaikkuna.columnconfigure(0, weight=1)

        self.framet = {}

        for F in (Aloitusframe, Peliframe, Asetusframe):
            frame = F(paaikkuna, self)
            self.framet[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.nayta_frame(Aloitusframe)

        self.peli = self.luo_peli()

    def nayta_frame(self, frame):
        frame1 = self.framet[frame]
        frame1.tkraise()

    def luo_peli(self):
        return Peli.palauta_testipeli()


class Aloitusframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ttk.Label(self, text="UNO Card Game")
        label.grid(row=0, column=0, columnspan=3, sticky="nsew")

        nappi = ttk.Button(self, text="Peliframeen",
                           command=lambda: controller.nayta_frame(Peliframe))
        nappi.grid(row=1, column=0, sticky="nsew")

        nappi2 = ttk.Button(self, text="Asetukset",
                            command=lambda: controller.nayta_frame(Asetusframe))
        nappi2.grid(row=1, column=1, sticky="nsew")

        nappi3 = ttk.Button(self, text="Lopeta",
                            command=lambda: controller.quit())
        nappi3.grid(row=1, column=2, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


class Asetusframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ttk.Label(self, text="Asetusframe")
        label.grid(row=0, column=0, sticky="nsew")

        nappi = ttk.Button(self, text="Aloitusframeen",
                           command=lambda: controller.nayta_frame(Aloitusframe))
        nappi.grid(row=1, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)


class Peliframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tilastoframe = Tilastoframe(self)
        tilastoframe.grid(row=0, column=0, sticky="nsew")

        korttiframe = Korttiframe(self)
        korttiframe.grid(row=1, column=0, sticky="nsew")

        nappi = ttk.Button(self, text="Aloitusframeen",
                           command=lambda: self.controller.nayta_frame(Aloitusframe))
        nappi.grid(row=2, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)


class Tilastoframe(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.luo_widgetit()

    def luo_widgetit(self):
        label = ttk.Label(self, text="Tilastoframe")
        label.grid(row=0, column=0, sticky="nsew")


class Korttiframe(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.luo_widgetit()

    def luo_widgetit(self):

        label1 = ttk.Label(self, text="Syötä pelaajien nimet:")
        label1.grid(row=0, column=0, sticky="nsew")

        pelaaja_widgetit = []
        # Entryjen validointimetodi
        vcmd = (self.register(self.onValidate), '%P')
        for i in range(1, Config.PELAAJA_LKM + 1):
            pelaaja = tk.StringVar()
            label_pelaaja = ttk.Label(self, text=f"Pelaaja {i}")
            label_pelaaja.grid(row=i, column=0, sticky="nsew")

            entry_pelaaja = ttk.Entry(self, textvariable=pelaaja,
                                        validate='key', validatecommand=vcmd)
            entry_pelaaja.grid(row=i, column=1, sticky="nsew")

            pelaaja_widgetit.append((label_pelaaja, entry_pelaaja))

        # nappi = ttk.Button(self, text="Pelaa",
        #                    command=lambda: self.parent.controller.peli.kaynnista())
        nappi = ttk.Button(self, text="Pelaa",
                           command=lambda: self.kaynnista(pelaaja_widgetit))
        nappi.grid(row=10, column=1, sticky="nsew")

    def onValidate(self, P):
        """Validoidaan pelaajien nimet.
        Pelaajien nimiksi hyvaksytaan vain isoja tai pienia kirjaimia.
        Nimen maksimipituus on 11 merkkia.
        """
        valid = "abcdefghijklmnopqrstuvwxyzåäö"
        valid = valid + valid.upper() + "0123456789 "

        if len(P) > 15:
            return False

        for l in P:
            if l not in valid:
                return False
        return True

    def tarkista_tyhjat_nimikentat(self, pelaajat):
        laskuri = 1
        for _, pelaaja in pelaajat:
            if len(pelaaja.get()) < 1:
                pelaaja.insert(0, f"Pelaaja {laskuri}")
                laskuri += 1

    def kaynnista(self, pelaajat):
        self.tarkista_tyhjat_nimikentat(pelaajat)
        for _, pelaaja in pelaajat:
            print(pelaaja.get())

