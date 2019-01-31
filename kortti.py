from config import Config


class Kortti:
    """UNO-kortin luokka.
    """

    def __init__(self, arvo, vari, pisteet, toiminta=None):
        self.arvo = arvo
        self.vari = vari
        self.toiminta = toiminta
        self.pisteet = pisteet

    def get_pisteet(self):
        return self.pisteet

    def get_arvo(self):
        return self.arvo

    def get_image(self):
        path = "cards/"
        ext = ".png"
        special = "spc"
        if self.arvo <= 12:
            return f"{path}{str(self.arvo).zfill(2)}_{self.vari}{ext}"
        else:
            return f"{path}{str(self.arvo).zfill(2)}_{special}{ext}"

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
        color_dict = {k: v for v, k in enumerate(Config.KORTTIVARIT)}
        if color == Config.ERIKOISVARI:
            return len(color_dict)
        return color_dict[color]
