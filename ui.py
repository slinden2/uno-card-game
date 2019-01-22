from peli import Peli


class Kayttoliittyma:

    def __init__(self):
        self.peli = Peli.palauta_perus_peli()

    def kaynnista(self):
        self.peli.luo_pelaajat()
        self.peli.pelaa_peli()
