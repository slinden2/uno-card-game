import tkinter as tk
import tkinter.font as tkFont
import webbrowser
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
        self.show_frame(MainScreen)

    def luo_framet(self):
        self.framet = {}
        for F in (MainScreen, PlayerPage, Asetusframe, GamePage, HelpPage):
            frame = F(self.main_window, self)
            self.framet[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame):
        if frame in (PlayerPage, GamePage):
            # pelaaja- ja peliframet taytyy paivittaa ennen nayttamista
            self.paivita_frame(frame)
        frame1 = self.framet[frame]
        frame1.tkraise()

    def update_frames(self):
        for frame in self.framet:
            self.framet[frame].destroy()
        self.luo_framet()

    def paivita_frame(self, frame):
        self.framet[frame].destroy()
        frame1 = frame(self.main_window, self)
        self.framet[frame] = frame1
        frame1.grid(row=0, column=0, sticky="nsew")


class MainScreen(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.set_logo()
        self.create_title()
        self.create_buttons()

    def set_logo(self):
        logo = tk.PhotoImage(file=Config.LOGO)
        logo_label = tk.Label(self, image=logo)
        logo_label.image = logo

        logo_label.grid(row=0, column=0)

    def create_title(self):
        font = tkFont.Font(**Config.TITLE_FONT)
        title_label = tk.Label(self, text="CARD GAME", font=font)
        title_label.grid(row=1, column=0, sticky="ew")

    def create_buttons(self):
        # set up dict for button creation
        button_properties = {"Play": lambda: self.controller.show_frame(PlayerPage),
                             "Settings": lambda: self.controller.show_frame(Asetusframe),
                             "Help": lambda: self.controller.show_frame(HelpPage),
                             "Quit": self.controller.quit}

        # create buttons
        for i, (text, command) in enumerate(button_properties.items(), start=2):
            button = ttk.Button(self,
                            text=text,
                            command=command,
                            width=30)
            button.grid(row=i, column=0, sticky="ns", pady=5)

            self.rowconfigure(i, weight=5)


class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        """Rules of the game
        """
        super().__init__(parent)

        self.controller = controller

        for i in range(0, 12):
            self.rowconfigure(i, weight=1)

        self.rowconfigure(12, weight=20)
        self.columnconfigure(0, weight=1)

        self.create_title()
        self.create_content()
        self.create_button()

    def create_title(self):
        """Title of the page
        """
        font = tkFont.Font(**Config.TITLE_FONT)

        label1 = ttk.Label(self, text="Help", font=font)
        label1.grid(row=0, column=0)

    def create_content(self):
        """Create content widgets
        """
        # set up title widge
        title_font = tkFont.Font(**Config.HELP_TITLE)
        title_label = tk.Label(self, text="Rules", font=title_font, padx=10)
        title_label.grid(row=1, column=0, sticky="w")

        # set up first paragraphs
        for i, paragraph in enumerate((Config.PARAGRAPH_1,
                                       Config.PARAGRAPH_2,
                                       Config.PARAGRAPH_3), start=2):
            content = tk.Message(self, text=paragraph, aspect=1500, padx=10)
            content.grid(row=i, column=0, sticky="w")

        # set up bullet points
        for i, bullet in enumerate((Config.BULLET_1,
                                    Config.BULLET_2,
                                    Config.BULLET_3), start=5):
            bullet = tk.Label(self, text=bullet)
            bullet.grid(row=i, column=0, sticky="w", padx=20)

        # set up last paragraphs
        for i, paragraph in enumerate((Config.PARAGRAPH_4,
                                       Config.PARAGRAPH_5), start=8):
            content = tk.Label(self, text=paragraph, padx=10)
            content.grid(row=i, column=0, sticky="w")

        # create a table
        table = HelpTable(self, Config.HELP_TABLE)
        table.grid(row=10, column=0, sticky="w", padx=20)

        # create a link to wikipedia source page
        link = tk.Label(self, text=Config.LINK_TEXT, cursor="hand2", padx=20)
        link.grid(row=11, column=0, sticky="w")
        link.bind("<Button-1>", self.open_webbrowser)

    def create_button(self):
        """"Back to MainScreen button
        """
        button = ttk.Button(self, text="Back", command=self.back_to_mainscreen, width=30)
        button.grid(row=12, column=0)

    def back_to_mainscreen(self):
        self.controller.show_frame(MainScreen)

    @staticmethod
    def open_webbrowser(event):
        """Used for opening the Wikipedia source page
        """
        webbrowser.open(Config.HELP_LINK)


class HelpTable(tk.Frame):

    def __init__(self, parent, data):
        super().__init__(parent)
        self.borderwidth = 1
        self.data = data
        self.create_table()

    def create_table(self):
        title_font = tkFont.Font(**Config.HELP_TABLE_TITLE)
        for row_n, row_data in enumerate(self.data):
            for column_n, cell_data in enumerate(row_data): 

                if row_n % 2 == 0:
                    # every other row with different bgcolor
                    frame = tk.Frame(self,
                                     borderwidth=1,
                                     background="#DADADA",
                                     relief="groove",
                                     padx=5)
                else:
                    frame = tk.Frame(self,
                                     borderwidth=1,
                                     relief="groove",
                                     padx=5)

                frame.grid(row=row_n, column=column_n, sticky="nsew")

                if row_n == 0:
                    # first row with bold font
                    message = tk.Message(frame,
                                         text=cell_data,
                                         aspect=500,
                                         font=title_font,
                                         background="#DADADA")
                elif row_n % 2 == 0:
                    # every other row with different bgcolor
                    message = tk.Message(frame,
                                         text=cell_data,
                                         aspect=500,
                                         background="#DADADA")
                else:
                    message = tk.Message(frame, text=cell_data, aspect=500)

                message.pack(side="left")


class Asetusframe(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.columnconfigure(0, weight=1)

        self.create_title()
        self.create_label_frame()
        self.create_setting_widgets()
        self.create_buttons()

    def create_title(self):
        font = tkFont.Font(**Config.TITLE_FONT)
        title_label = tk.Label(self, text="Settings", font=font)
        title_label.grid(row=0, column=0, sticky="nsew")

    def create_label_frame(self):
        self.label_frame = ttk.LabelFrame(self, padding=10)
        self.label_frame.grid(row=1, column=0)

    def create_setting_widgets(self):
        # set up variables for setting labels and spinboxes
        font = tkFont.Font(**Config.SETTING_FONT)
        self.player_qty = tk.IntVar()
        self.player_qty.set(Config.PLAYER_QTY)
        self.winning_points = tk.IntVar()
        self.winning_points.set(Config.WINNING_POINTS)

        widget_properties = {"Player Quantity": {"increment": 1,
                                                 "from_": 2,
                                                 "to": 4,
                                                 "state": "readonly",
                                                 "wrap": True,
                                                 "textvariable": self.player_qty,
                                                 "width": 5},
                             "Winning Points": {"increment": 1,
                                                 "from_": 20,
                                                 "to": 500,
                                                 "wrap": True,
                                                 "textvariable": self.winning_points,
                                                 "width": 5}}

        # create widgets
        for i, setting in enumerate(widget_properties):
            label = tk.Label(self.label_frame, text=setting, font=font)
            label.grid(row=i, column=0, sticky="e", padx=20)

            spinbox = tk.Spinbox(self.label_frame, **widget_properties[setting], font=font)
            spinbox.grid(row=i, column=1, sticky="w", padx=20)

    def create_buttons(self):
        button_properties = [{"text": "OK",
                             "command": self.save_settings},
                            {"text": "Cancel",
                             "command": self.undo_changes}]

        for i, kwargs in enumerate(button_properties):
            button = ttk.Button(self.label_frame, **kwargs, width=30)
            button.grid(row=i, column=2)

    def undo_changes(self):
        """Cancel all the changes and go back to main screen.
        """
        self.player_qty.set(Config.PLAYER_QTY)
        self.winning_points.set(Config.WINNING_POINTS)
        self.controller.show_frame(MainScreen)

    def save_settings(self):
        """Save changes and go back to main screen.
        """
        Config.PLAYER_QTY = self.player_qty.get()
        Config.WINNING_POINTS = self.winning_points.get()
        self.controller.update_frames()
        self.controller.show_frame(MainScreen)


class PlayerPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.columnconfigure(0, weight=1)
        self.padding = 10

        self.create_title()
        self.create_label_frame()
        self.create_player_widgets()
        self.create_buttons()

    def create_title(self):
        font = tkFont.Font(**Config.TITLE_FONT)
        title_label = tk.Label(self, text="Players", font=font)
        title_label.grid(row=0, column=0, sticky="nsew")

    def create_label_frame(self):
        self.label_frame = ttk.LabelFrame(self, padding=10)
        self.label_frame.grid(row=1, column=0)

    def create_player_widgets(self):
        font = tkFont.Font(**Config.SETTING_FONT)
        self.player_widgets = []

        # entry validation method
        vcmd = (self.register(self.on_validate), '%P')

        # iterate over the player qty in order to create the correct
        # number of entry widgets
        for i in range(0, Config.PLAYER_QTY):
            label_text = "Player" if i == 0 else "Computer"
            player_name = tk.StringVar()
            player_label = tk.Label(self.label_frame,
                                    text=label_text,
                                    font=font)
            player_label.grid(row=i,
                              column=0,
                              sticky="nsw",
                              pady=self.padding,
                              padx=self.padding)

            player_entry = ttk.Entry(self.label_frame,
                                      textvariable=player_name,
                                      validate='key',
                                      validatecommand=vcmd,
                                      font=font)
            player_entry.grid(row=i,
                              column=1,
                              sticky="nsew",
                              pady=self.padding,
                              padx=self.padding)

            self.player_widgets.append((player_label, player_entry))

    def create_buttons(self):
        button_properties = {0: {"text": "Back",
                                 "command": lambda: self.controller.show_frame(MainScreen)},
                             1: {"text": "Play",
                                 "command": lambda: self.start(self.player_widgets)}}

        for column in button_properties:
            button = ttk.Button(self.label_frame, **button_properties[column])
            # row number 4 because the max number of players is 4. The buttons
            # will be positioned under the entry widgets.
            button.grid(row=4, column=column, sticky="nsew", padx=10)

    def on_validate(self, P):
        """Validates the player names in the entry widgets.
        The names can have only small or capital letters or numbers.
        Max length of the name is 15 chars.
        """
        valid = "abcdefghijklmnopqrstuvwxyzåäö"
        valid = valid + valid.upper() + "0123456789 "

        if len(P) > 15:
            return False

        for l in P:
            if l not in valid:
                return False
        return True

    def check_empty_entries(self, players):
        """If some of the entry widgets are left empty,
        this method will fill a default name in the field.

        :param players: A list of entry widgets
        """
        count = 1
        for label, player_entry in players:
            if len(player_entry.get()) < 1:
                if label.cget("text") == "Player":
                    player_entry.insert(0, "Pelaaja")
                else:
                    player_entry.insert(0, f"Computer {count}")
                    count += 1

    def start(self, players):
        """Start the game

        :param players: A list of entry widgets
        """
        self.check_empty_entries(players)

        # create player
        self.controller.peli.luo_pelaaja(players[0][1].get(), False)

        # create computers
        for _, computer in players[1:]:
            self.controller.peli.luo_pelaaja(computer.get(), True)

        self.controller.peli.aloita_ensimmainen_peli()
        self.controller.peli_kaynnissa = True
        self.controller.show_frame(GamePage)


class GamePage(tk.Frame):

    def __init__(self, parent, controller):
        """This class contains the actual game frame and all functionality
        that is linked to the game logic.
        """
        super().__init__(parent)
        self.controller = controller

        self.create_stat_frame()
        self.create_table_frame()

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=20)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

    def create_stat_frame(self):
        self.tilastoframe = StatFrame(self, self.controller)
        self.tilastoframe.grid(row=0, column=0, sticky="nsew")

    def create_table_frame(self):
        """Table refers to an actual table where the game 
        is to be played
        """
        self.korttiframe = Korttiframe(self, self.controller)
        self.korttiframe.grid(row=1, column=0, sticky="nsew")

    def paivita_tilastoframe(self):
        self.tilastoframe.destroy()
        self.create_stat_frame()

    def paivita_korttiframe(self):
        self.korttiframe.destroy()
        self.create_table_frame()

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


class StatFrame(tk.Frame):

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
        self.controller.update_frames()
        self.controller.show_frame(MainScreen)

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
