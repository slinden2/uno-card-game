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
        self.hand = []

    def draw_card(self, kortti):
        """Lisaa kortin self.hand -listaan
        :param kortti: :class:`Kortti`
        """
        if kortti:
            self.hand.append(kortti)

    def hae_kortti(self, arvo, vari):
        for kortti in self.hand:
            if kortti.arvo == arvo and kortti.vari == vari:
                return kortti
        print("Kädessä ei ole kyseistä korttia.")
        return -1

    def play_turn(self, kortti):
        """Poistaa kortin kädestä.
        :param kortti: :class:`Kortti`
        """
        if kortti != -1:
            self.hand.remove(kortti)
            return kortti

    def get_name(self):
        return self.nimi

    def get_last_card(self):
        return self.hand[-1]

    def get_hand(self):
        return self.hand

    def tulosta_kasi(self):
        for i, kortti in enumerate(self.get_hand(), start=1):
            print(f"    {i:>2} - {kortti}")

    def destroy_hand(self):
        self.hand[:] = []

    def wins(self):
        self.voitot += 1

    def lisaa_pisteita(self, pisteet):
        self.pisteet += pisteet

    def get_points(self):
        return self.pisteet

    def is_computer(self):
        return self.tietokone

    def resetoi(self):
        self.destroy_hand()
        self.pisteet = 0
        self.voitot = 0

    def __str__(self):
        return f"Nimi: {self.nimi} - Käsi: {[str(kortti) for kortti in self.hand]}"
