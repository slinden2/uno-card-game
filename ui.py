import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from peli import Peli
from config import Config


class UnoCardGame(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1024x768+16+100")
        self.configure(background="green")
        self.resizable(width=False, height=False)
        self.iconbitmap(Config.ICON)

        tk.Tk.wm_title(self, "UNO Card Game")

        self.main_window = tk.Frame(self)
        self.main_window.pack(side="top", fill="both", expand=True)

        self.main_window.rowconfigure(0, weight=1)
        self.main_window.columnconfigure(0, weight=1)

        self.peli = Peli()
        self.peli_kaynnissa = False

        self.framet = {}
        self.luo_framet()
        self.nayta_frame(Aloitusframe)

    def luo_framet(self):
        self.framet = {}
        for F in (Aloitusframe, Pelaajaframe, Asetusframe, Peliframe):
            frame = F(self.main_window, self)
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
        frame1 = frame(self.main_window, self)
        self.framet[frame] = frame1
        frame1.grid(row=0, column=0, sticky="nsew")


class Aloitusframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=5)
        self.rowconfigure(4, weight=5)
        self.columnconfigure(0, weight=1)

        self.set_logo()
        self.set_title()
        self.create_buttons()

    def set_logo(self):
        logo = tk.PhotoImage(file=Config.LOGO)
        logo_label = tk.Label(self, image=logo)
        logo_label.image = logo

        logo_label.grid(row=0, column=0)

    def set_title(self):
        font = tkFont.Font(family="Helvetica", size=50, weight="bold")

        label = tk.Label(self, text="CARD GAME", font=font)
        label.grid(row=1, column=0, sticky="ew")

    def create_buttons(self):
        methods = {"Play": lambda: self.controller.nayta_frame(Pelaajaframe),
                   "Settings": lambda: self.controller.nayta_frame(Asetusframe),
                   "Quit": self.controller.quit}

        for i, (text, command) in enumerate(methods.items(), start=2):
            nappi = ttk.Button(self,
                            text=text,
                            command=command,
                            width=30)
            nappi.grid(row=i, column=0, sticky="ns")


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
        entry_pelaaja_maara = tk.Spinbox(self,
                                         increment=1,
                                         from_=2,
                                         to=4,
                                         state="readonly",
                                         wrap=True,
                                         textvariable=self.pelaaja_lkm)
        entry_pelaaja_maara.grid(row=1, column=1, sticky="ew")

        label1 = ttk.Label(self, text="Voittopisteet")
        label1.grid(row=2, column=0, sticky="nsew")

        self.voittopisteet = tk.IntVar()
        self.voittopisteet.set(Config.VOITTOPISTEET)
        entry_voittopisteet = tk.Spinbox(self,
                                         increment=1,
                                         from_=20,
                                         to=500,
                                         wrap=True,
                                         textvariable=self.voittopisteet)
        entry_voittopisteet.grid(row=2, column=1, sticky="ew")

        nappi1 = ttk.Button(self,
                            text="Peruuta",
                            command=self.peruuta_muutokset)
        nappi1.grid(row=3, column=0, sticky="nsew")

        nappi2 = ttk.Button(self,
                            text="OK",
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

            entry_pelaaja = ttk.Entry(self,
                                      textvariable=pelaaja,
                                      validate='key',
                                      validatecommand=vcmd)
            entry_pelaaja.grid(row=i, column=1, sticky="nsew")

            pelaaja_widgetit.append((label_pelaaja, entry_pelaaja))

        nappi1 = ttk.Button(self,
                            text="Aloitusframeen",
                            command=lambda: self.controller.nayta_frame(Aloitusframe))
        nappi1.grid(row=10, column=0, sticky="nsew")

        nappi2 = ttk.Button(self,
                            text="Pelaa",
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

        self.controller.peli.aloita_ensimmainen_peli()
        self.controller.peli_kaynnissa = True
        self.controller.nayta_frame(Peliframe)


class Peliframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.luo_tilastoframe()
        self.luo_korttiframe()

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=20)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

    def luo_tilastoframe(self):
        self.tilastoframe = Tilastoframe(self, self.controller)
        self.tilastoframe.grid(row=0, column=0, sticky="nsew")

    def luo_korttiframe(self):
        self.korttiframe = Korttiframe(self, self.controller)
        self.korttiframe.grid(row=1, column=0, sticky="nsew")

    def paivita_tilastoframe(self):
        self.tilastoframe.destroy()
        self.luo_tilastoframe()

    def paivita_korttiframe(self):
        self.korttiframe.destroy()
        self.luo_korttiframe()

    def paivita_peliframe(self):
        self.paivita_tilastoframe()
        self.paivita_korttiframe()

    def lopeta_vuoro(self):
        if self.controller.peli.peli_pelattu:
            self.paivita_tilastoframe()
            self.paivita_korttiframe()
            self.controller.peli_kaynnissa = False

        elif (self.controller.peli.vuoro_pelattu_tietokone or
              self.controller.peli.kortti_nostettu or
              self.controller.peli.kierros_pelattu or
              self.controller.peli.kysytaan_varia):
            self.paivita_korttiframe()
            self.paivita_tilastoframe()

        # while loopia tarvitaan erityisesti kaksinpelissä, jos
        # tietokone pelaa enemmän kuin yhden vuoronskippauskortin
        # peräkkäin
        while (self.controller.peli.ohitus and not
               self.controller.peli.kierros_pelattu and not
               self.controller.peli.kysytaan_varia):
            self.controller.peli.ohita_pelaajan_vuoro()
            self.paivita_korttiframe()
            self.paivita_tilastoframe()


class Tilastoframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)

        self.luo_widgetit()
        self.luo_feed_widget()
        self.luo_hallintanapit()

    def luo_widgetit(self):

        value_pad = 10

        labelframe = ttk.LabelFrame(self, text="Tilastot")
        labelframe.grid(row=0, column=0, rowspan=2, padx=5, sticky="nsew")

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

    def luo_feed_widget(self):

        self.feed_frame = ttk.LabelFrame(self, text="Feed")
        self.feed_frame.grid(row=0, column=1, rowspan=2, padx=5, sticky="nsew")

        self.feed_frame.columnconfigure(0, weight=50)
        self.feed_frame.columnconfigure(1, weight=1)
        self.feed_frame.rowconfigure(0, weight=1)

        self.pystyscroll = ttk.Scrollbar(self.feed_frame)
        self.pystyscroll.grid(row=0, column=1, sticky="nsw")

        self.feed_box = tk.Listbox(self.feed_frame,
                                   activestyle="dotbox",
                                   height=7,
                                   yscrollcommand=self.pystyscroll.set,
                                   highlightthickness=0)
        self.feed_box.grid(row=0, column=0, sticky="nsew")
        self.pystyscroll["command"] = self.feed_box.yview

        for timestamp in self.controller.peli.feed.messages:
            msg = " - ".join(timestamp)
            self.feed_box.insert(tk.END, msg)
            self.feed_box.yview(tk.END)

    def luo_hallintanapit(self):
        if not self.controller.peli.peli_pelattu:
            tila = tk.NORMAL
            if not self.controller.peli.kierros_pelattu:
                tila = tk.DISABLED
            kierros_nappi = ttk.Button(self,
                                       text="Seuraava kierros",
                                       command=self.aloita_seuraava_kierros,
                                       state=tila)
            kierros_nappi.grid(row=0, column=2, sticky="ew")
        else:
            uusi_peli_nappi = ttk.Button(self,
                                         text="Uusi peli",
                                         command=self.aloita_uusi_peli)
            uusi_peli_nappi.grid(row=0, column=2, sticky="ew")

        lopeta_nappi = ttk.Button(
            self, text="Lopeta peli", command=self.lopeta_peli)
        lopeta_nappi.grid(row=1, column=2, sticky="ew")

    def aloita_seuraava_kierros(self):
        self.controller.peli.aloita_uusi_kierros()
        self.parent.paivita_tilastoframe()
        self.parent.paivita_korttiframe()
        self.parent.lopeta_vuoro()

    def aloita_uusi_peli(self):
        self.controller.peli.aloita_uusi_peli()
        self.controller.peli_kaynnissa = True
        self.parent.paivita_peliframe()

    def lopeta_peli(self):
        self.controller.peli = Peli()
        self.controller.peli_kaynnissa = False
        self.controller.paivita_framet()
        self.controller.nayta_frame(Aloitusframe)

    def paivita_feed(self):
        self.feed_frame.destroy()
        self.luo_feed_widget()


class Korttiframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        self.rowconfigure(0, weight=11)
        self.rowconfigure(1, weight=17)
        self.rowconfigure(2, weight=11)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=15)
        self.columnconfigure(2, weight=15)
        self.columnconfigure(3, weight=10)

        if not self.controller.peli.kierros_pelattu:
            self.luo_widgetit()

            if (self.controller.peli.kysytaan_varia and
                    self.controller.peli.vuorossa == 0):
                self.kysy_varia()

    def luo_widgetit(self):

        if self.controller.peli_kaynnissa:
            pakkaframe = Pakkaframe(self, self.controller)
            pakkaframe.grid(row=1, column=1, columnspan=2, sticky="nsew")

            self.aseta_aloituskadet()

    def lataa_kuva(self,
                   frame,
                   kortti=None,
                   nostopakka=False,
                   poistopakka=False,
                   oikea=False,
                   yla=False):
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
        kuva_label = Kuvalabel(frame,
                               self.controller,
                               image=kuva,
                               binding=binding,
                               name=name)
        kuva_label.image = kuva
        return kuva_label

    def aseta_aloituskadet(self):
        self.luo_korttiframet()
        for i, (pelaaja, frame) in enumerate(zip(self.controller.peli.pelaajat,
                                                 self.korttiframet)):
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
                frame = tk.Frame(self, borderwidth=1, padx=10)
                # luodaan tyhja labeli, muuten jostain syysta vaakakortit sisallaan
                # pitavat rivit jaavat liian mataliksi
                label = tk.Label(frame, text=" ", height=4)
                label.pack()
            else:
                # pystytasossa olevat kadet
                frame = tk.Frame(self, borderwidth=1, pady=10)

            if i == 0:
                frame.grid(row=3, column=1, columnspan=2, sticky="nsew")
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

    def kysy_varia(self):
        vari_frame = tk.Frame(self)
        vari_frame.grid(row=2, column=1, columnspan=2, sticky="ew")

        vari_label = ttk.Label(vari_frame, text="Kysyttävä väri: ")
        vari_label.grid(row=0, column=0)
        vari_label.rowconfigure(0, weight=1)
        vari_label.columnconfigure(0, weight=1)

        for i, vari in enumerate(self.controller.peli.varit, start=1):
            # lambda vari=vari tallentaa vari-muuttujan arvon eri iterointikierroksilta
            # jos vari=varia ei kayteta, niin metodi kutsutaan aina for-loopin
            # viimeisen kierroksen arvolla
            nappi = ttk.Button(vari_frame,
                               text=vari,
                               command=lambda vari=vari: self.kasittele_vari(vari))
            nappi.grid(row=0, column=i)

    def kasittele_vari(self, vari):
        self.controller.peli.vastaanota_vari(vari)
        self.parent.paivita_tilastoframe()
        self.parent.paivita_korttiframe()
        self.parent.lopeta_vuoro()


class Pakkaframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.master = parent
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        if not self.controller.peli.nostopakka.on_tyhja():
            self.aseta_nostopakka()

        self.aseta_poistopakan_kortti()

    def aseta_nostopakka(self):
        kuva_label = self.master.lataa_kuva(self, nostopakka=True)
        kuva_label.grid(row=0, column=0)

    def aseta_poistopakan_kortti(self):
        kortti = self.controller.peli.poistopakka.get_viimeinen_kortti()
        kuva_label = self.master.lataa_kuva(
            self, kortti=kortti, poistopakka=True)
        kuva_label.grid(row=0, column=1)


class Kuvalabel(tk.Label):

    def __init__(self, parent, controller, binding=False, name="", **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.controller = controller
        self.name = name

        # varivalinnan aikana disabloidaan muut komennot
        if binding and not self.controller.peli.kysytaan_varia:
            self.bind("<Button-1>", self.valitse_toiminto)

    def valitse_toiminto(self, event):
        if self.name == "nostopakka":
            self.nosta_kortti()
        elif self.name == "poistopakka":
            self.passaa()
        elif self.name == "kasi":
            self.pelaa_kortti()

        self.parent.master.parent.lopeta_vuoro()

    def passaa(self):
        self.controller.peli.passaa()

    def nosta_kortti(self):
        self.controller.peli.nosta_kortti()

    def pelaa_kortti(self):
        indeksi = self.winfo_name()[-1:]
        indeksi = int(indeksi) - 1 if indeksi != "l" else 0
        self.controller.peli.pelaa_kortti(indeksi)

        # Kaikki toimintakortit toimii

        # Lisaa feediin ilmoitus koko pelin loppumisesta
