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

        self.paaikkuna = tk.Frame(self)
        self.paaikkuna.pack(side="top", fill="both", expand=True)

        self.paaikkuna.rowconfigure(0, weight=1)
        self.paaikkuna.columnconfigure(0, weight=1)

        self.peli = Peli()

        self.framet = {}
        self.luo_framet()
        self.nayta_frame(Aloitusframe)

    def luo_framet(self):
        self.framet = {}
        for F in (Aloitusframe, Peliframe, Asetusframe):
            frame = F(self.paaikkuna, self)
            self.framet[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def nayta_frame(self, frame):
        frame1 = self.framet[frame]
        frame1.tkraise()

    def paivita_framet(self):
        for frame in self.framet:
            self.framet[frame].destroy()
        self.luo_framet()

    # def paivita_frame(self):
    #     self.framet[Peliframe].destroy()
    #     del self.framet[Peliframe]

    #     frame = Peliframe(self.paaikkuna, self)
    #     self.framet[Peliframe] = frame
    #     frame.grid(row=0, column=0, sticky="nsew")


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

        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.luo_widgetit()

    def luo_widgetit(self):
        label1 = ttk.Label(self, text="Asetukset")
        label1.grid(row=0, column=0, columnspan=2, sticky="nsew")

        label1 = ttk.Label(self, text="Pelaajamäärä")
        label1.grid(row=1, column=0, sticky="nsew")

        self.pelaaja_lkm = tk.IntVar()
        self.pelaaja_lkm.set(Config.PELAAJA_LKM)
        entry_pelaaja_maara = tk.Spinbox(
            self, increment=1, from_=2, to=4, state="readonly", wrap=True, textvariable=self.pelaaja_lkm)
        entry_pelaaja_maara.grid(row=1, column=1, sticky="ew")

        label1 = ttk.Label(self, text="Voittopisteet")
        label1.grid(row=2, column=0, sticky="nsew")

        self.voittopisteet = tk.IntVar()
        self.voittopisteet.set(Config.VOITTOPISTEET)
        entry_voittopisteet = tk.Spinbox(
            self, increment=1, from_=20, to=500, wrap=True, textvariable=self.voittopisteet)
        entry_voittopisteet.grid(row=2, column=1, sticky="ew")

        nappi1 = ttk.Button(self, text="Peruuta",
                            command=self.peruuta_muutokset)
        nappi1.grid(row=3, column=0, sticky="nsew")

        nappi2 = ttk.Button(self, text="OK",
                            command=self.tallenna_asetukset)
        nappi2.grid(row=3, column=1, sticky="nsew")

    def peruuta_muutokset(self):
        self.pelaaja_lkm.set(Config.PELAAJA_LKM)
        self.voittopisteet.set(Config.VOITTOPISTEET)
        self.controller.nayta_frame(Aloitusframe)

    def tallenna_asetukset(self):
        Config.PELAAJA_LKM = self.pelaaja_lkm.get()
        Config.VOITTOPISTEET = self.voittopisteet.get()
        self.controller.paivita_framet()
        self.controller.nayta_frame(Aloitusframe)


class Peliframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tilastoframe = Tilastoframe(self)
        tilastoframe.grid(row=0, column=0, sticky="nsew")

        pelaajaframe = Pelaajaframe(self)
        pelaajaframe.grid(row=1, column=0, sticky="nsew")

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
        self.parent = parent

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.luo_widgetit()

    def luo_widgetit(self):

        labelframe = ttk.LabelFrame(self, text="Tilastot")
        labelframe.grid(row=0, column=0, columnspan=2, sticky="nsew")

        label1 = tk.Label(labelframe, text="Kierros")
        label1.grid(row=0, column=0, sticky="nsew")

        kierros = tk.IntVar()
        kierros.set(self.parent.controller.peli.kierros)
        label2 = tk.Label(labelframe, textvariable=kierros)
        label2.grid(row=0, column=1, sticky="nsew")

        for i, pelaaja in enumerate(self.parent.controller.peli.pelaajat, start=1):
            nimi = tk.StringVar()
            nimi.set(pelaaja.get_nimi())
            label3 = tk.Label(labelframe, textvariable=nimi)
            label3.grid(row=i, column=0, sticky="nsew")

            pisteet = tk.IntVar()
            pisteet.set(pelaaja.get_pisteet())
            label4 = tk.Label(labelframe, textvariable=pisteet)
            label4.grid(row=i, column=1, sticky="nsew")


class Pelaajaframe(tk.Frame):

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
        """Jos jokin pelaajista jää nimeättä, tämä metodi
        täyttää nimikentän.
        """
        laskuri = 1
        for _, pelaaja in pelaajat:
            if len(pelaaja.get()) < 1:
                pelaaja.insert(0, f"Pelaaja {laskuri}")
                laskuri += 1

    def kaynnista(self, pelaajat):
        self.tarkista_tyhjat_nimikentat(pelaajat)

        for _, pelaaja in pelaajat:
            self.parent.controller.peli.luo_pelaaja(pelaaja.get())

        self.parent.controller.peli.pelaa_peli()
