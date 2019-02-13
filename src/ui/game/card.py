import tkinter as tk


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
