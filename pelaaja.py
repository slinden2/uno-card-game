class Player:
    """Class for handling players of UNO Card Game.
    The class allows to retain name, points, wins
    and the current hand of the player in memory.

    The cards in the hand are Card objects.

    :param name: Players name
    :param computer: True if the player is not controlled
                     by a human player.
    """

    def __init__(self, name, computer=False):
        self.name = name
        self.computer = computer
        self.points = 0
        self.win_num = 0
        self.hand = []

    def draw_card(self, card):
        """Adds a card to self.hand list
        :param card: :class:`Card`
        """
        if card:
            self.hand.append(card)

    def search_card(self, value, color):
        """Search a card in hand based on its value and color.
        """
        for card in self.hand:
            if card.get_value() == value and card.get_color() == color:
                return card
        print(f"{self.name} doesn't have that card.")
        return -1

    def play_turn(self, card):
        """Poistaa kortin kädestä.
        :param card: :class:`Card`
        """
        if card != -1:
            self.hand.remove(card)
            return card

    def get_name(self):
        return self.name

    def get_last_card(self):
        return self.hand[-1]

    def get_hand(self):
        return self.hand

    def print_hand(self):
        for i, kortti in enumerate(self.get_hand(), start=1):
            print(f"    {i:>2} - {kortti}")

    def destroy_hand(self):
        self.hand[:] = []

    def wins(self):
        self.win_num += 1

    def add_points(self, points):
        self.points += points

    def get_points(self):
        return self.points

    def is_computer(self):
        return self.computer

    def resetoi(self):
        self.destroy_hand()
        self.points = 0
        self.win_num = 0

    def __str__(self):
        return f"Name: {self.name} - Hand: {[str(kortti) for card in self.hand]}"
