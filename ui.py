import tkinter as tk
from tkinter import ttk
from peli import Peli
from config import Config


class UnoCardGame(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1024x768+16+100")
        self.configure(background="green")
        self.resizable(width=False, height=False)

        tk.Tk.wm_title(self, "UNO Card Game")

        self.paaikkuna = tk.Frame(self)
        self.paaikkuna.pack(side="top", fill="both", expand=True)

        self.paaikkuna.rowconfigure(0, weight=1)
        self.paaikkuna.columnconfigure(0, weight=1)

        self.peli = Peli()
        self.peli_kaynnissa = False

        self.framet = {}
        self.luo_framet()
        self.nayta_frame(Aloitusframe)

    def luo_framet(self):
        self.framet = {}
        for F in (Aloitusframe, Pelaajaframe, Asetusframe, Peliframe):
            frame = F(self.paaikkuna, self)
            self.framet[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def nayta_frame(self, frame):
        if frame in (Pelaajaframe, Peliframe):
            # pelaaja- ja peliframet taytyy paivittaa ennen nayttamista
            self.paivita_frame(frame)
        frame1 = self.framet[frame]
        frame1.tkraise()

    def paivita_framet(self):
        for frame in self.framet:
            self.framet[frame].destroy()
        self.luo_framet()

    def paivita_frame(self, frame):
        self.framet[frame].destroy()
        frame1 = frame(self.paaikkuna, self)
        self.framet[frame] = frame1
        frame1.grid(row=0, column=0, sticky="nsew")


class Aloitusframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ttk.Label(self, text="UNO Card Game")
        label.grid(row=0, column=0, columnspan=3, sticky="nsew")

        nappi = ttk.Button(self, text="Pelaajaframeen",
                           command=lambda: controller.nayta_frame(Pelaajaframe))
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


class Pelaajaframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

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

        nappi1 = ttk.Button(self, text="Aloitusframeen",
                            command=lambda: self.controller.nayta_frame(Aloitusframe))
        nappi1.grid(row=10, column=0, sticky="nsew")

        nappi2 = ttk.Button(self, text="Pelaa",
                            command=lambda: self.kaynnista(pelaaja_widgetit))
        nappi2.grid(row=10, column=1, sticky="nsew")

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
        # luodaan pelaaja
        self.controller.peli.luo_pelaaja(pelaajat[0][1].get(), False)
        # luodaan tietokoneet
        for _, pelaaja in pelaajat[1:]:
            self.controller.peli.luo_pelaaja(pelaaja.get(), True)

        self.controller.peli.pelaa_peli()
        self.controller.peli_kaynnissa = True
        self.controller.nayta_frame(Peliframe)


class Peliframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tilastoframe = Tilastoframe(self)
        tilastoframe.grid(row=0, column=0, sticky="nsew")

        self.korttiframe = Korttiframe(self, self.controller)
        self.korttiframe.grid(row=1, column=0, sticky="nsew")

        nappi = ttk.Button(self, text="Lopeta peli",
                           command=self.lopeta_peli)
        nappi.grid(row=2, column=0, sticky="nsew")

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=20)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

    def lopeta_peli(self):
        self.controller.peli = Peli()
        self.controller.peli_kaynnissa = False
        self.controller.paivita_framet()
        self.controller.nayta_frame(Aloitusframe)

    # TODO
    # def paivita_pakat(self):
    #     self.korttiframe.destroy()
    #     self.korttiframe = Korttiframe(self, self.controller)
    #     self.korttiframe.grid(row=1, column=0, sticky="nsew")


class Tilastoframe(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.luo_widgetit()

    def luo_widgetit(self):

        value_pad = 10

        labelframe = ttk.LabelFrame(self, text="Tilastot")
        labelframe.grid(row=0, column=0, columnspan=2, sticky="nsew")

        label1 = tk.Label(labelframe, text="Kierros")
        label1.grid(row=0, column=0, sticky="w")

        kierros = tk.IntVar()
        kierros.set(self.parent.controller.peli.kierros)
        label2 = tk.Label(labelframe, textvariable=kierros)
        label2.grid(row=0, column=1, sticky="w", padx=value_pad)

        for i, pelaaja in enumerate(self.parent.controller.peli.pelaajat, start=1):
            nimi = tk.StringVar()
            nimi.set(pelaaja.get_nimi())
            label3 = tk.Label(labelframe, textvariable=nimi)
            label3.grid(row=i, column=0, sticky="w")

            pisteet = tk.IntVar()
            pisteet.set(pelaaja.get_pisteet())
            label4 = tk.Label(labelframe, textvariable=pisteet)
            label4.grid(row=i, column=1, sticky="w", padx=value_pad)


class Korttiframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        self.rowconfigure(0, weight=11)
        self.rowconfigure(1, weight=17)
        self.rowconfigure(2, weight=11)
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=15)
        self.columnconfigure(2, weight=15)
        self.columnconfigure(3, weight=10)

        self.luo_widgetit()

    def luo_widgetit(self):

        if self.controller.peli_kaynnissa:

            self.aseta_nostopakka()
            self.aseta_poistopakan_kortti()
            self.aseta_aloituskadet()

    def aseta_nostopakka(self):
        kuva_label = self.lataa_kuva(self, nostopakka=True)
        kuva_label.grid(row=1, column=1)

    def aseta_poistopakan_kortti(self):
        kortti = self.controller.peli.poistopakka.get_viimeinen_kortti()
        kuva_label = self.lataa_kuva(self, kortti=kortti, poistopakka=True)
        kuva_label.grid(row=1, column=2)

    def lataa_kuva(self, frame, kortti=None, nostopakka=False, poistopakka=False, oikea=False, yla=False):
        binding = False
        name = ""
        if nostopakka:
            kuva = tk.PhotoImage(file=Config.KORTIN_TAKA_NORMAALI)
            binding = True
            name = "nostopakka"
        if yla:
            kuva = tk.PhotoImage(file=Config.KORTIN_TAKA_YLA)
        elif oikea and not yla:
            kuva = tk.PhotoImage(file=Config.KORTIN_TAKA_OIKEA)
        elif not oikea and not yla and not nostopakka:
            kuva = tk.PhotoImage(file=Config.KORTIN_TAKA_VASEN)
        if kortti:
            kuva = tk.PhotoImage(file=kortti.get_image())
            binding = True
            name = "kasi" if not poistopakka else "poistopakka"
        kuva_label = Kuvalabel(frame, self.controller,
                               image=kuva, binding=binding, name=name)
        kuva_label.image = kuva
        return kuva_label

    def aseta_aloituskadet(self):
        self.luo_korttiframet()
        for i, (pelaaja, frame) in enumerate(zip(self.controller.peli.pelaajat, self.korttiframet)):
            if i == 0:
                self.aseta_vaaka_kasi(frame, pelaaja)
            elif i == 1:
                self.aseta_pysty_kasi(frame, pelaaja)
            elif i == 2:
                self.aseta_pysty_kasi(frame, pelaaja, oikea=True)
            elif i == 3:
                self.aseta_vaaka_kasi(frame, pelaaja, yla=True)

    def luo_korttiframet(self):
        self.korttiframet = []
        for i in range(0, 4):

            if i == 0 or i == 3:
                # vaakatasossa olevat kadet
                frame = tk.Frame(self, borderwidth=1, relief="sunken", padx=10)
                # luodaan tyhja labeli, muuten jostain syysta vaakakortit sisallaan
                # pitavat rivit jaavat liian mataliksi
                label = tk.Label(frame, text=" ", height=4)
                label.pack()
            else:
                # pystytasossa olevat kadet
                frame = tk.Frame(self, borderwidth=1, relief="sunken", pady=10)

            if i == 0:
                frame.grid(row=2, column=1, columnspan=2, sticky="nsew")
            elif i == 1:
                frame.grid(row=1, column=0, sticky="nsew")
            elif i == 2:
                frame.grid(row=1, column=3, sticky="nsew")
            elif i == 3:
                frame.grid(row=0, column=1, columnspan=2, sticky="nsew")

            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            self.korttiframet.append(frame)

    def aseta_vaaka_kasi(self, frame, pelaaja, yla=False):
        for i, kortti in enumerate(pelaaja.get_kasi()):
            if yla:
                kuva = self.lataa_kuva(frame, yla=yla)
                kuva.place(x=i*45, y=147, anchor="sw")
            else:
                kuva = self.lataa_kuva(frame, kortti=kortti)
                kuva.place(x=i*45, y=155, anchor="sw")

    def aseta_pysty_kasi(self, frame, pelaaja, oikea=False):
        for i, _ in enumerate(pelaaja.get_kasi()):
            kuva = self.lataa_kuva(frame, oikea=oikea)
            if oikea:
                kuva.place(x=15, y=i*15, anchor="nw")
            else:
                kuva.place(x=0, y=i*15, anchor="nw")

    def paivita_pakat(self):
        for child in self.winfo_children():
            child.destroy()
        self.luo_widgetit()


class Kuvalabel(tk.Label):

    def __init__(self, parent, controller, binding=False, name="", **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.controller = controller
        self.name = name

        if binding:
            self.bind("<Button-1>", self.valitse_toiminto)

    def valitse_toiminto(self, event):
        if self.name == "nostopakka":
            self.nosta_kortti()
        elif self.name == "poistopakka":
            self.passaa()
        elif self.name == "kasi":
            self.pelaa_kortti()

    def passaa(self):
        self.controller.peli.passaa()
        if self.controller.peli.vuoro_pelattu_tietokone:
            self.parent.paivita_pakat()

    def nosta_kortti(self):
        self.controller.peli._nosta_kortti()
        if self.controller.peli.kortti_nostettu:
            self.parent.paivita_pakat()

    def pelaa_kortti(self):
        indeksi = self.winfo_name()[-1:]
        indeksi = int(indeksi) - 1 if indeksi != "l" else 0
        self.controller.peli.pelaa_vuoro(indeksi)
        if self.controller.peli.vuoro_pelattu_tietokone:
            self.parent.master.paivita_pakat()

        # jatka tietokoneen vuoronpelaamisalgoritmia

        # kortin nosto ja passaus ei vielä toimi. kierroksen alustusajankohta
        # ja tarvittavat muuttujat työn alla
