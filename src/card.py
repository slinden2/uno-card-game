from config import Config


class Card:
    """UNO card
    """

    def __init__(self, value, color, points, action=None):
        self.value = value
        self.color = color
        self.action = action
        self.points = points

    def get_points(self):
        return self.points

    def get_value(self):
        return self.value

    def get_image(self):
        path = "cards/"
        ext = ".png"
        special = "spc"
        if self.value <= 12:
            return f"{path}{str(self.value).zfill(2)}_{self.color}{ext}"
        else:
            return f"{path}{str(self.value).zfill(2)}_{special}{ext}"

    def compare_color(self, other):
        """Returns True if the color of the cards is the same.
        """
        return self.color == other.color

    def compare_value(self, other):
        """Returns True if the value of the cards is the same.
        """
        return self.value == other.value

    def compare_to_wildcard(self, wildcard_color):
        """Returns True if the color of the card corresponds
        to the wildcard color."""
        return self.color == wildcard_color

    def is_wildcard(self):
        """Returns True if the 'color' of the card is wildcard.
        """
        return self.color == Config.SPECIAL_COLOR

    def __str__(self):
        return f"{self.value} {self.color}{' ' + self.action if self.action else ''}"

    def __repr__(self):
        return f"Card({self.value}, {self.color}, {self.points}, {self.action})"

    def __lt__(self, other):
        if self._quantify_color(self.color) < self._quantify_color(other.color):
            return True

        if self.value < other.value and \
            (self._quantify_color(self.color) ==
             self._quantify_color(other.color)):
            return True

        return False

    @staticmethod
    def _quantify_color(color):
        """Gives a number for the card colors so that they
        can be sorted.
        """
        color_dict = {k: v for v, k in enumerate(Config.CARD_COLORS)}
        if color == Config.SPECIAL_COLOR:
            return len(color_dict)
        return color_dict[color]
