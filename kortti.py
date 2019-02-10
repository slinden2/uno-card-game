from config import Config


class Kortti:
    """UNO-kortin luokka.
    """

    def __init__(self, arvo, vari, pisteet, toiminta=None):
        self.arvo = arvo
        self.vari = vari
        self.toiminta = toiminta
        self.pisteet = pisteet

    def get_points(self):
        return self.pisteet

    def get_value(self):
        return self.arvo

    def get_image(self):
        path = "cards/"
        ext = ".png"
        special = "spc"
        if self.arvo <= 12:
            return f"{path}{str(self.arvo).zfill(2)}_{self.vari}{ext}"
        else:
            return f"{path}{str(self.arvo).zfill(2)}_{special}{ext}"

    def compare_color(self, other):
        """Returns True if the color of the cards is the same.
        """
        return self.vari == other.vari

    def compare_value(self, other):
        """Returns True if the value of the cards is the same.
        """
        return self.arvo == other.arvo

    def compare_to_wildcard(self, wildcard_color):
        """Returns True if the color of the card corresponds
        to the wildcard color."""
        return self.vari == wildcard_color

    def is_wildcard(self):
        """Returns True if the 'color' of the card is wildcard.
        """
        return self.vari == Config.SPECIAL_COLOR

#   # TODO tee tarkastusmetodit korttiluokkaan
# if (pelattu_kortti.vari == verrattava_kortti.vari or
#     pelattu_kortti.arvo == verrattava_kortti.arvo or
#     pelattu_kortti.vari == Config.SPECIAL_COLOR or
#         pelattu_kortti.vari == self.jokerivari):
#     return True

    def __str__(self):
        return f"{self.arvo} {self.vari}{' ' + self.toiminta if self.toiminta else ''}"

    def __repr__(self):
        return f"Kortti({self.arvo}, {self.vari}, {self.pisteet}, {self.toiminta})"

    def __lt__(self, other):
        if self._quantify_color(self.vari) < self._quantify_color(other.vari):
            return True
        if self.arvo < other.arvo and \
            (self._quantify_color(self.vari) ==
             self._quantify_color(other.vari)):
            return True
        return False

    @staticmethod
    def _quantify_color(color):
        color_dict = {k: v for v, k in enumerate(Config.CARD_COLORS)}
        if color == Config.SPECIAL_COLOR:
            return len(color_dict)
        return color_dict[color]
