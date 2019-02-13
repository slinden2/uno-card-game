import tkinter as tk

from config import Config

from ui.game.deck import DeckFrame
from ui.game.card import CardLabel
from ui.game.query_color import QueryColorFrame


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
            self.query_color()

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
            image = tk.PhotoImage(file=Config.BACK_OF_CARD_NORMAL)
            binding = True
            name = "draw_deck"
        if top:
            image = tk.PhotoImage(file=Config.BACK_OF_CARD_TOP)
        elif right and not top:
            image = tk.PhotoImage(file=Config.BACK_OF_CARD_RIGHT)
        elif not any((right, top, draw_deck)):
            image = tk.PhotoImage(file=Config.BACK_OF_CARD_LEFT)
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
        mapper = {
            0: lambda frame, player: self.set_horizontal_hand(frame, player),
            1: lambda frame, player: self.set_vertical_hand(frame, player),
            2: lambda frame, player: self.set_vertical_hand(frame, player, right=True),
            3: lambda frame, player: self.set_horizontal_hand(frame, player, top=True)
        }

        self.create_card_frames()
        for i, (player, frame) in enumerate(zip(self.controller.game.players,
                                                self.card_frames)):
            mapper[i](frame, player)

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
        color_frame = QueryColorFrame(self,
                                      self.controller)
        color_frame.grid(row=2, column=2, sticky="nsew")
