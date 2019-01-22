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

    def __str__(self):
        return f"{self.arvo:<2} {self.vari}{' ' + self.toiminta if self.toiminta else ''}"
