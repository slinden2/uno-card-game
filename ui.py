import tkinter as tk
import tkinter.font as tkFont
import webbrowser
from tkinter import ttk
from peli import Game
from config import Config


class UnoCardGame(tk.Tk):

    def __init__(self, *args, **kwargs):
        """Controller class of the app.
        """
        super().__init__(*args, **kwargs)

        self.geometry("1024x768+16+100")
        self.resizable(width=False, height=False)
        self.iconbitmap(Config.ICON)

        tk.Tk.wm_title(self, "UNO Card Game")

        self.main_window = tk.Frame(self)
        self.main_window.pack(side="top", fill="both", expand=True)

        self.main_window.rowconfigure(0, weight=1)
        self.main_window.columnconfigure(0, weight=1)

        self.game = Game()
        self.game_on = False

        self.frames = {}
        self.create_frames()
        self.show_frame(MainScreen)

    def create_frames(self):
        """Create frames and a controller dict.
        """
        self.frames = {}
        for F in (MainScreen, PlayerPage, Asetusframe, GamePage, HelpPage):
            frame = F(self.main_window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame):
        """Show a frame if found in controller dict.

        :param frame: Frame to be shown.
        """
        if frame in (PlayerPage, GamePage):
            # player and game frames must be updated before showing
            self.update_frame(frame)
        frame1 = self.frames[frame]
        frame1.tkraise()

    def update_frames(self):
        """Destroy all the frames and recreate them.
        """
        for frame in self.frames:
            self.frames[frame].destroy()
        self.create_frames()

    def update_frame(self, frame):
        """Destroy a frame and recreate it.
        """
        self.frames[frame].destroy()
        frame1 = frame(self.main_window, self)
        self.frames[frame] = frame1
        frame1.grid(row=0, column=0, sticky="nsew")


class MainScreen(tk.Frame):

    def __init__(self, parent, controller):
        """Main menu
        """
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
        self.controller.game.create_player(players[0][1].get(), False)

        # create computers
        for _, computer in players[1:]:
            self.controller.game.create_player(computer.get(), True)

        self.controller.game.start_first_game()
        self.controller.game_on = True
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

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.columnconfigure(0, weight=1)

    def create_stat_frame(self):
        """Stat frame is the frame that contains the feed and 
        the points of the players.
        """
        self.stat_frame = StatFrame(self, self.controller)
        self.stat_frame.grid(row=0, column=0, sticky="nsew")

    def create_table_frame(self):
        """Table refers to an actual table where the game 
        is to be played
        """
        self.table_frame = TableFrame(self, self.controller)
        self.table_frame.grid(row=1, column=0, sticky="nsew")

    def update_stat_frame(self):
        self.stat_frame.destroy()
        self.create_stat_frame()

    def update_table_frame(self):
        self.table_frame.destroy()
        self.create_table_frame()

    def update_peliframe(self):
        self.update_stat_frame()
        self.update_table_frame()

    def end_turn(self):
        """After every turn all the frames are updated
        so that the changes become visible to the user."""
        if self.controller.game.game_played:
            self.update_stat_frame()
            self.update_table_frame()
            self.controller.game_on = False

        elif (self.controller.game.turn_played_computer or
              self.controller.game.card_drawn or
              self.controller.game.round_played or
              self.controller.game.color_queried):
            self.update_table_frame()
            self.update_stat_frame()

        # while loop is needed for skipping the players
        # turn if more than one skip turn card is played
        while (self.controller.game.passing and not
               self.controller.game.round_played and not
               self.controller.game.color_queried):
            self.controller.game.pass_players_turn()
            self.update_table_frame()
            self.update_stat_frame()


class StatFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)

        self.create_title()
        self.create_point_widget()
        self.create_feed_widget()
        self.create_buttons()

    def create_title(self):
        """Create changing round number title at the top of the page.
        """
        font = tkFont.Font(**Config.ROUND_FONT)
        round_num_str = tk.StringVar()
        round_num_str.set(f"Round {self.parent.controller.game.round_num}")
        label2 = tk.Label(self, textvariable=round_num_str, font=font)
        label2.grid(row=0, column=0, columnspan=3, sticky="nsew")

    def create_point_widget(self):
        """Show player points during the game. The points update after
        every round.
        """
        font = tkFont.Font(**Config.POINT_FONT)
        point_frame = ttk.LabelFrame(self, text="Points")
        point_frame.grid(row=1, column=0, rowspan=2, padx=5, sticky="nsew")

        for i, player in enumerate(self.parent.controller.game.players):
            player_name = tk.StringVar()
            player_name.set(player.get_name())
            name_label = tk.Label(point_frame, textvariable=player_name, font=font)
            name_label.grid(row=i, column=0, sticky="w")

            points = tk.IntVar()
            points.set(player.get_points())
            point_label = tk.Label(point_frame, textvariable=points, font=font)
            point_label.grid(row=i, column=1, sticky="w", padx=10)

    def create_feed_widget(self):
        """Create the feed box that shows what happens during computers
        turns.
        """
        self.feed_frame = ttk.LabelFrame(self, text="Feed")
        self.feed_frame.grid(row=1, column=1, rowspan=2, padx=5, sticky="nsew")

        self.feed_frame.columnconfigure(0, weight=50)
        self.feed_frame.columnconfigure(1, weight=1)
        self.feed_frame.rowconfigure(0, weight=1)

        # scrollbar that activates when the feed box has
        # enough content
        self.vert_scroll = ttk.Scrollbar(self.feed_frame)
        self.vert_scroll.grid(row=0, column=1, sticky="nsw")

        self.feed_box = tk.Listbox(self.feed_frame,
                                   activestyle="dotbox",
                                   height=7,
                                   yscrollcommand=self.vert_scroll.set,
                                   highlightthickness=0)
        self.feed_box.grid(row=0, column=0, sticky="nsew")

        # set the scrollbar to control the feed boxes yview method
        self.vert_scroll["command"] = self.feed_box.yview

        # insert messages to the feed box
        for timestamp in self.controller.game.feed.messages:
            msg = " - ".join(timestamp)
            self.feed_box.insert(tk.END, msg)
            self.feed_box.yview(tk.END)

    def create_buttons(self):
        """Create next round, new game and quit buttons.
        """
        # create next round or new game buttons depending on
        # the state of the game
        if not self.controller.game.game_played:
            state = tk.NORMAL

            if not self.controller.game.round_played:
                state = tk.DISABLED

            round_button = ttk.Button(self,
                                       text="Next round",
                                       command=self.start_next_round,
                                       state=state)
            round_button.grid(row=1, column=2, sticky="ew")

        else:
            new_game_button = ttk.Button(self,
                                         text="New game",
                                         command=self.start_new_game)
            new_game_button.grid(row=1, column=2, sticky="ew")

        quit_button = ttk.Button(self,
                                  text="Quit",
                                  command=self.quit_game)
        quit_button.grid(row=2, column=2, sticky="ew")

    def start_next_round(self):
        self.controller.game.start_new_round()
        self.parent.update_stat_frame()
        self.parent.update_table_frame()
        self.parent.end_turn()

    def start_new_game(self):
        self.controller.game.start_new_game()
        self.controller.game_on = True
        self.parent.update_game_page()

    def quit_game(self):
        self.controller.game = Game()
        self.controller.game_on = False
        self.controller.update_frames()
        self.controller.show_frame(MainScreen)

    def update_feed(self):
        self.feed_frame.destroy()
        self.create_feed_widget()


class TableFrame(tk.Frame):

    def __init__(self, parent, controller):
        """Table refers to an actual table with the cards on it.
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        if not self.controller.game.round_played:
            self.create_deck_frame()
            self.query_color()  # TODO

            # TODO
            # if (self.controller.game.color_queried and
            #         self.controller.game.in_turn == 0):
            #     self.query_color()

    def create_deck_frame(self):

        if self.controller.game_on:
            deck_frame = DeckFrame(self, self.controller)
            deck_frame.grid(row=1, column=1, sticky="nsew")

            self.set_starting_hands()

    def load_image(self,
                   frame,
                   card=None,
                   draw_deck=False,
                   discard_deck=False,
                   right=False,
                   top=False):
        """Load image files that represent the UNO cards.
        The if statements define which card image to load in base of
        the position of a player.

        :param frame: The parent frame where the image will be positioned.
        :param card: Defines that the card is in the players hand.
        :param draw_deck: Defines that the card is in the draw deck.
        :param discard_deck: Defines that the card is in the discard deck.
        :param right: Defines that the card is in the second computers hand.
        :param top: Defines that the card is in the third computers hand.

        :returns: An ImageLabel object
        """
        # define wether a card is clickable or not
        binding = False

        # name defines a which method is called from the game logic
        # when a clickable card is clicked
        name = ""
        if draw_deck:
            image = tk.PhotoImage(file=Config.KORTIN_TAKA_NORMAALI)
            binding = True
            name = "draw_deck"
        if top:
            image = tk.PhotoImage(file=Config.KORTIN_TAKA_YLA)
        elif right and not top:
            image = tk.PhotoImage(file=Config.KORTIN_TAKA_OIKEA)
        elif not right and not top and not draw_deck:
            image = tk.PhotoImage(file=Config.KORTIN_TAKA_VASEN)
        if card:
            image = tk.PhotoImage(file=card.get_image())
            binding = True
            name = "hand" if not discard_deck else "discard_deck"
        card_label = CardLabel(frame,
                               self.controller,
                               image=image,
                               binding=binding,
                               name=name)
        card_label.image = image
        return card_label

    def set_starting_hands(self):
        """Create and position starting hands for all players.
        """
        self.create_card_frames()
        for i, (player, frame) in enumerate(zip(self.controller.game.players,
                                                 self.card_frames)):
            if i == 0:
                self.set_horizontal_hand(frame, player)
            elif i == 1:
                self.set_vertical_hand(frame, player)
            elif i == 2:
                self.set_vertical_hand(frame, player, right=True)
            elif i == 3:
                self.set_horizontal_hand(frame, player, top=True)

    def create_card_frames(self):
        """Create empty frames to hold the hands of the players.
        """
        self.card_frames = []
        for i in range(0, 4):

            if i == 0 or i == 3:
                # horizontal decks
                frame = tk.Frame(self, padx=10, width="130m", height="51m")
                # create an empty label because otherwise the frame
                # containing the deck remains too low.
                # label = tk.Label(frame, text=" ")
                # label.pack()
            else:
                # vertical decks
                frame = tk.Frame(self, pady=10)

            if i == 0:
                frame.grid(row=2, column=1, sticky="nsew")
            elif i == 1:
                frame.grid(row=1, column=0, sticky="nsew")
            elif i == 2:
                frame.grid(row=1, column=2, sticky="nsew")
            elif i == 3:
                frame.grid(row=0, column=1, sticky="nsew")

            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            frame.grid_propagate(0)
            self.card_frames.append(frame)

    def set_horizontal_hand(self, frame, player, top=False):
        """Create a horizontal hand for the player and
        the third computer.

        :param frame: The parent frame
        :param player: A Player object
        :param top: Defines that the hand is for the third computer.
        """
        player_name = tk.StringVar()
        for i, card in enumerate(player.get_hand()):

            if top:
                player_name.set(self.controller.game.players[-1].get_name())
                label = tk.Label(frame, textvariable=player_name)
                label.grid(row=0, column=0, sticky="s")
                image = self.load_image(frame, top=top)
                image.place(x=i*45, y=160, anchor="sw")

            else:
                player_name.set(self.controller.game.players[0].get_name())
                label = tk.Label(frame, textvariable=player_name)
                label.grid(row=0, column=0, sticky="n")
                image = self.load_image(frame, card=card)
                image.place(x=i*45, y=188, anchor="sw")

    def set_vertical_hand(self, frame, player, right=False):
        """Create a horizontal hand for the player and
        the third computer.

        :param frame: The parent frame
        :param player: A Player object
        :param right: Defines that the hand is for the second computer.
        """
        player_name = tk.StringVar()
        for i, _ in enumerate(player.get_hand()):

            image = self.load_image(frame, right=right)

            if right:
                player_name.set(self.controller.game.players[2].get_name())
                label = tk.Label(frame, textvariable=player_name, wraplength=1)
                label.grid(row=0, column=0, sticky="w")

                # don't show more than 7 cards due to lack of space
                if i < 7:
                    image.place(x=35, y=i*15, anchor="nw")

            else:
                player_name.set(self.controller.game.players[1].get_name())
                label = tk.Label(frame, textvariable=player_name, wraplength=1)
                label.grid(row=0, column=0, sticky="e")

                if i < 7:
                    image.place(x=0, y=i*15, anchor="nw")

    def query_color(self):
        color_frame = QueryColorFrame(self, self.controller)
        color_frame.grid(row=2, column=2, sticky="nsew")


class DeckFrame(tk.Frame):

    def __init__(self, parent, controller):
        """Contains the two decks in the middle of the table.
        """
        super().__init__(parent,
                         relief="sunken",
                         borderwidth=1)
        self.parent = parent
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.create_labels()

        if not self.controller.game.draw_deck.on_tyhja():
            self.set_draw_deck()

        self.discard_first_card()

    def create_labels(self):
        draw_label = tk.Label(self, text="Draw")
        draw_label.grid(row=0, column=0)

        pass_label = tk.Label(self, text="Pass")
        pass_label.grid(row=0, column=1)

        # display num of cards left in the draw deck
        num_of_cards = tk.IntVar()
        num_of_cards.set(self.controller.game.draw_deck.cards_left())
        num_of_cards_label = tk.Label(self, textvariable=num_of_cards)
        num_of_cards_label.grid(row=2, column=0)

    def set_draw_deck(self):
        card_label = self.parent.load_image(self, draw_deck=True)
        card_label.grid(row=1, column=0)

    def discard_first_card(self):
        card = self.controller.game.discard_deck.get_last_card()
        card_label = self.parent.load_image(self,
                                             card=card,
                                             discard_deck=True)
        card_label.grid(row=1, column=1)


class CardLabel(tk.Label):

    def __init__(self, parent, controller, binding=False, name="", **kwargs):
        """Contains a specific card and all related functionality.

        :param parent: The parent of the frame
        :param controller: The controller frame of the app.
        :param binding: Set to True if the card has a callback.
        :param name: Describes the funcionality of the card.
                        -draw_deck = Player draws a card.
                        -discard_deck = Player passes a turn.
                        -hand = Player plays a card.
        """
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.controller = controller
        self.name = name

        # while the player is choosing the wild card color, all other
        # functionalitt is disabled.
        if binding and not self.controller.game.color_queried:
            self.bind("<Button-1>", self.choose_action)

    def choose_action(self, event):
        if self.name == "draw_deck":
            self.draw_card()
        elif self.name == "discard_deck":
            self.pass_turn()
        elif self.name == "hand":
            self.play_card()

        self.parent.master.parent.end_turn()

    def pass_turn(self):
        """Player passes.
        """
        self.controller.game.pass_turn()

    def draw_card(self):
        """Player attempts to draw a card.
        """
        self.controller.game.draw_card()

    def play_card(self):
        """Player attempts to play a card.
        """
        index = self.winfo_name()[-1:]
        index = int(index) - 1 if index != "l" else 0
        self.controller.game.play_card(index)


class QueryColorFrame(tk.Frame):

    def __init__(self, parent, controller):
        """Contains functionality related to choosing 
        the wild card color.
        """
        super().__init__(parent, width="10m")

        self.parent = parent
        self.controller = controller

        self.grid_propagate(0)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.rowconfigure(2, weight=20)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        if (self.controller.game.color_queried and
            self.controller.game.in_turn == 0):
            self.create_title()
            self.create_buttons()

    def create_title(self):
        label = ttk.Label(self, text="Choose a color")
        label.grid(row=0, column=0, columnspan=2)

    def create_buttons(self):
        button_grid_properties = {0: {"row": 1,
                                      "column": 0,
                                      "sticky": "nsew"},
                                  1: {"row": 1,
                                      "column": 1,
                                      "sticky": "nsew"},
                                  2: {"row": 2,
                                      "column": 0,
                                      "sticky": "nsew"},
                                  3: {"row": 2,
                                      "column": 1,
                                      "sticky": "nsew"}}
    
        for i, color in enumerate(self.controller.game.draw_deck.get_varit()):
    
            # translate command colors to actual colors supported by tcl
            button_color = {"red": "red",
                            "yel": "yellow",
                            "gre": "green",
                            "blu": "blue"}

            # lambda color=color stores the value of the color variable after
            # every iteration. If color=color is not defined, the value of the
            # color will be the same for every button. The value would be
            # the last value of the iteration.
            button = tk.Button(self,
                               background=button_color[color],
                               command=lambda color=color: self.process_color(color))
            button.grid(**button_grid_properties[i])

    def process_color(self, color):
        """Send the chosen wild card color to the game logic.
        """
        self.controller.game.receive_color(color)
        self.parent.parent.update_stat_frame()
        self.parent.parent.update_table_frame()
        self.parent.parent.end_turn()
    