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
