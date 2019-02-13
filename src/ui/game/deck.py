import tkinter as tk


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

        if not self.controller.game.draw_deck.is_empty():
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
