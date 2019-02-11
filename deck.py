import random
from config import Config
from card import Card


class Deck:
    """Contains an UNO card deck.

    A deck contains:
        -19 red cards 0-9
        -19 yellow cards 0-9
        -19 green cards 0-9
        -19 blue cards 0-9
        -8 skip cards
        -8 reverse cards
        -8 draw 2 cards
        -4 wild cards
        -4 wild card/draw 4 cards
    """

    def __init__(self):
        self.deck = []
        self.colors = Config.CARD_COLORS
        self.created = False
        self.action_cards = {10: "skip",
                               11: "reverse",
                               12: "draw 2",
                               13: "wild card",
                               14: "wild card + 4"}

    def create_deck(self):
        if self.created:
            self.deck[:] = []
            self.created = False
        self._create_zero_cards()
        self._create_color_cards()
        self._create_color_cards()
        self._create_wild_cards()
        self.created = True

    def _create_zero_cards(self):
        for color in self.colors:
            self.deck.append(Card(0, color, 0))

    def _create_color_cards(self):
        """Create cards 0-9 for all 4 colors of the game.

        The method creates also 3 action cards per color.
            -1 skip card (10)
            -1 reverse card (11)
            -1 draw 2 card (12)
        """
        for color in self.colors:
            for i in range(1, 13):
                if i < 10:
                    self.deck.append(
                        Card(i, color, i, self.action_cards.get(i, None)))
                else:
                    self.deck.append(
                        Card(i, color, 20, self.action_cards.get(i, None)))

    def _create_wild_cards(self):
        """Create 8 wild cards:
            -4 wild cards (13)
            -4 wild card / draw 4 cards (14)
        """
        for i in range(13, 15):
            for _ in range(0, 4):
                self.deck.append(
                    Card(i, Config.SPECIAL_COLOR, 50, self.action_cards.get(i, None)))

    def shuffle(self):
        random.shuffle(self.deck)

    def get_deck(self):
        return self.deck

    def get_colors(self):
        return self.colors

    def deal_card(self):
        if not self.is_empty():
            return self.deck.pop(0)
        else:
            print("The deck is empty.")
            return False

    def add_card(self, card):
        self.deck.append(card)

    def turn_deck(self):
        self.deck = self.deck[::-1]

    def get_last_card(self):
        return self.deck[-1]

    def is_empty(self):
        return len(self) == 0

    def cards_left(self):
        return len(self)

    def __len__(self):
        return len(self.deck)

    def __str__(self):
        return f"{[str(card) for card in self.deck]}"
