class Pelaaja:
    """Luokka UNO-korttipelin pelaajien hallintaan.
    Luokan avulla voidaan pitää muistissa pelaajan nimi,
    pisteet, voitot ja kädessä olevat kortit.

    Kädessa olevien korttien on tarkoitus olla Kortti-luokan olioita.

    :param nimi: Pelaajan nimi
    """

    def __init__(self, nimi, tietokone=False):
        self.nimi = nimi
        self.tietokone = tietokone
        self.pisteet = 0
        self.voitot = 0
        self.kasi = []

    def nosta_kortti(self, kortti):
        """Lisaa kortin self.kasi -listaan
        :param kortti: :class:`Kortti`
        """
        if kortti:
            self.kasi.append(kortti)

    def hae_kortti(self, arvo, vari):
        for kortti in self.kasi:
            if kortti.arvo == arvo and kortti.vari == vari:
                return kortti
        print("Kädessä ei ole kyseistä korttia.")
        return -1

    def pelaa_vuoro(self, kortti):
        """Poistaa kortin kädestä.
        :param kortti: :class:`Kortti`
        """
        if kortti != -1:
            self.kasi.remove(kortti)
            return kortti

    def get_nimi(self):
        return self.nimi

    def get_viimeinen_kortti(self):
        return self.kasi[-1]

    def get_kasi(self):
        return self.kasi

    def tulosta_kasi(self):
        for i, kortti in enumerate(self.get_kasi(), start=1):
            print(f"    {i:>2} - {kortti}")

    def tuhoa_kasi(self):
        self.kasi[:] = []

    def voittaa(self):
        self.voitot += 1

    def lisaa_pisteita(self, pisteet):
        self.pisteet += pisteet

    def get_pisteet(self):
        return self.pisteet

    def __str__(self):
        return f"Nimi: {self.nimi} - Käsi: {[str(kortti) for kortti in self.kasi]}"
