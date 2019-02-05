import random
from config import Config
from kortti import Kortti


class Pakka:
    """UNO-korttipakan sisällään pitävä luokka.
    Pakassa on 108 korttia:
        -19 punaista korttia 0-9
        -19 keltaista korttia 0-9
        -19 vihreää korttia 0-9
        -19 sinistä korttia 0-9
        -8 ohituskorttia
        -8 suunnanvaihtokorttia
        -8 nosta kaksi -korttia
        -4 jokerikorttia
        -4 jokeri- + nosta neljä -korttia
    """

    def __init__(self):
        self.korttipakka = []
        self.varit = Config.KORTTIVARIT
        self.luotu = False
        self.toimintakortit = {10: "ohitus",
                               11: "suunnanvaihto",
                               12: "nosta 2",
                               13: "jokeri",
                               14: "jokeri + 4"}

    # TODO apumetodi korttien testamiseen
    # def luo_pakka(self):
    #     for i in range(0, 50):
    #         self.korttipakka.append(Kortti(0, "blu", 0))
    #     self.luotu = True

    def luo_pakka(self):
        if self.luotu:
            self.korttipakka[:] = []
            self.luotu = False
        self._luo_nollakortit()
        self._luo_varikortit()
        self._luo_varikortit()
        # self._luo_erikoiskortit()  # TODO testausta varten
        self.luotu = True

    def _luo_nollakortit(self):
        for vari in self.varit:
            self.korttipakka.append(Kortti(0, vari, 0))

    def _luo_varikortit(self):
        """Luo kortit 0-9 neljälle UNO-pelin värille.
        Tämän lisäksi metodi luo jokaiselle värille kolme toimintakorttia:
            -1 ohituskortti (arvo 10)
            -1 suunnanvaihtokortti (arvo 11)
            -1 nosta 2 -kortti (arvo 12)
        """
        for vari in self.varit:
            # TODO muokattu testausta varten. Oikea arvo 1, 13.
            for i in range(1, 11):
                if i < 10:
                    self.korttipakka.append(
                        Kortti(i, vari, i, self.toimintakortit.get(i, None)))
                else:
                    for _ in range(0, 1):  # TODO poista for loop
                        self.korttipakka.append(
                            Kortti(i, vari, 20, self.toimintakortit.get(i, None)))

    def _luo_erikoiskortit(self):
        """Luo kahdeksan toimintakorttia:
            -4 jokeria (värinvaihtokortti, arvo 13)
            -4 jokeri + nosta 4 -korttia (pitää sisällään värinvaihdon, arvo 14)
        """
        for i in range(13, 15):
            for _ in range(0, 4):
                self.korttipakka.append(
                    Kortti(i, Config.ERIKOISVARI, 50, self.toimintakortit.get(i, None)))

    def sekoita(self):
        random.shuffle(self.korttipakka)

    def get_pakka(self):
        return self.korttipakka

    def get_varit(self):
        return self.varit

    def jaa_kortti(self):
        if len(self.korttipakka) > 1:
            return self.korttipakka.pop(0)
        else:
            print("Pakassa ei ole kortteja!")
            return False

    def lisaa_kortti(self, kortti):
        self.korttipakka.append(kortti)

    def kaanna_pakka(self):
        self.korttipakka = self.korttipakka[::-1]

    def get_viimeinen_kortti(self):
        return self.korttipakka[-1]

    def __len__(self):
        return len(self.korttipakka)

    def __str__(self):
        return f"{[str(kortti) for kortti in self.korttipakka]}"
