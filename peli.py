from config import Config
from pakka import Pakka
from pelaaja import Pelaaja


class Peli:
    """Tämä luokka pitää sisällään UNO-korttipelin logiikan.
    Peli-olion saa helposti luotua oletusasetuksilla kutsumalla
    Peli.palauta_perus_peli()-metodin. Oletuksena on 3 pelaajaa ja
    voittoon tarvitaan 500 pistettä.

    :param: pelaajien_lkm: Pelaajien lukumäärä
    :param: voittopisteet: Voittoon tarvittavien pisteiden määrä
    """

    def __init__(self, pelaajien_lkm, voittopisteet):
        self.pelaajien_lkm = pelaajien_lkm
        self.voittopisteet = voittopisteet
        self.pelaajat = []
        self.nostopakka = Pakka()
        self.poistopakka = Pakka()
        self.kierros = 1
        self.vuorossa = 0
        self.aloittaja = 0
        self.pelisuunta = 1
        self.kortti_nostettu = False
        self.vuoro_pelattu = False
        self.kierros_pelattu = False
        self.jokerivari = Config.ERIKOISVARI
        self.toimintakortin_pelannut_pelaaja = None

    @classmethod
    def palauta_perus_peli(cls):
        """3 pelaajaa ja voittoon varvittavat pisteet 500
        """
        return cls(2, 10)

    def luo_pelaajat(self):
        for pelaajanumero in range(1, self.pelaajien_lkm + 1):
            nimi = input(f"Syötä pelaajan {pelaajanumero} nimi: ")
            self.pelaajat.append(Pelaaja(nimi))
        print()

    def pelaa_peli(self):
        """Pelinhallintametodi
        Metodin suoritus loppuu, kun joku pelaajista saavuttaa
        voittoon tarvittavan pistemäärän.
        """
        print("Tervetuloa UNO-korttipeliin.")
        print()

        while True:
            # määritetään kierroksen kierroksen aloittava pelaaja
            if self.kierros > 1:
                self.maarita_aloittava_pelaaja()

            self.kierros_pelattu = False
            self.nostopakka.luo_pakka()
            self.nostopakka.sekoita()
            self.jaa_aloituskortit()
            self.nostopakka.kaanna_pakka()
            self.aloituskortti_poistopakkaan()
            self.pelaa_kierros()

            if self._tarkista_voittopisteet():
                break

    def maarita_aloittava_pelaaja(self):
        if self.aloittaja < len(self.pelaajat):
            self.aloittaja += 1
            self.vuorossa = self.aloittaja
        else:
            self.aloittaja, self.vuorossa = 0, 0

    def get_vuorossaoleva_pelaaja(self):
        return self.pelaajat[self.vuorossa]

    def get_seuraava_pelaaja(self):
        if self.pelisuunta == 1:

            if self.vuorossa < self.pelaajien_lkm - 1:
                return self.pelaajat[self.vuorossa + 1]
            else:
                return self.pelaajat[0]

        else:
            if self.vuorossa == 0:
                return self.pelaajat[self.pelaajien_lkm - 1]
            else:
                return self.pelaajat[self.vuorossa - 1]

    def seuraava_pelaaja(self):
        """Metodia käytetään vuoron vaihtamiseen."""
        if self.pelisuunta == 1:

            if self.vuorossa == self.pelaajien_lkm - 1:
                self.vuorossa = 0
            else:
                self.vuorossa += 1

        else:
            if self.vuorossa == 0:
                self.vuorossa = self.pelaajien_lkm - 1
            else:
                self.vuorossa -= 1

    def jaa_aloituskortit(self):
        """Jaetaan aloituskortit kaikille pelissä oleville
        pelaajille."""
        for _ in range(0, 7):
            for pelaaja in self.pelaajat:
                pelaaja.nosta_kortti(self.nostopakka.jaa_kortti())

    def aloituskortti_poistopakkaan(self):
        """Asetetaan aloituskortti poistopakkaan.
        Aloituskortti ei voi olla toimintakortti.
        """
        while True:
            aloituskortti = self.nostopakka.jaa_kortti()

            if aloituskortti.arvo > 9:
                self.nostopakka.lisaa_kortti(aloituskortti)
                continue

            self.poistopakka.lisaa_kortti(aloituskortti)
            break

    def tuhoa_pelaajien_kadet(self):
        """Jokaisen kierroksen päätyttyä pelaajien
        kädet täytyy nollata"""
        for pelaaja in self.pelaajat:
            pelaaja.tuhoa_kasi()

    def pelaa_kierros(self):
        """Yksittäinen kierros päättyy, kun jokin pelaajista
        saa pelattua kätensä viimeisen kortin.
        """
        print(f"{self.kierros:>2}. kierros")
        print("=" * 20)
        self.aloittaja = self.vuorossa

        while not self.kierros_pelattu:
            pelaaja = self.get_vuorossaoleva_pelaaja()
            self.toimintakortin_pelannut_pelaaja = None
            self.pelaa_vuoro()

            if self._tarkista_voitto():
                self._laske_voittopisteet()
                print(
                    f"{self.kierros:>2}. kierroksen voittaja on {pelaaja.get_nimi()}. Pisteet: {pelaaja.get_pisteet()}.")
                self.tuhoa_pelaajien_kadet()
                self.kierros_pelattu = True

            self.seuraava_pelaaja()
        input()

    def pelaa_vuoro(self):
        """Vuorometodi hallitsee pelaajan vaihtoehtoja.
        Pelaaja voi joko 
            -pelata kortin
            -nostaa kortin
            -passata
        """
        self.alusta_vuoro()
        print("Pelaajan käsi:")
        kadessa_olevat_kortit = self.tulosta_pelaajan_kortit()

        while not self.vuoro_pelattu:
            syote = self._pelaajan_syote()

            if syote == "N":
                self._nosta_kortti()
            elif syote == "P":
                self._passaa()
            else:
                kortti = kadessa_olevat_kortit[syote]
                self._pelaa_kortti(kortti)

        print()

    def alusta_vuoro(self):
        vika_kortti = self.poistopakka.get_viimeinen_kortti()
        print(f"Kysytty kortti on {vika_kortti}.")
        if vika_kortti.arvo >= 13:
            print(f"Jokeriväri on {self.jokerivari}.")

        pelaaja = self.get_vuorossaoleva_pelaaja()
        print(f"Vuorossa on {pelaaja.get_nimi()}.")
        self.vuoro_pelattu = False
        self.kortti_nostettu = False

    def _pelaajan_syote(self):
        syote = ""
        mahdolliset_syotteet = [str(x) for x in range(
            1, len(self.get_vuorossaoleva_pelaaja().get_kasi()) + 1)] + ["N", "P"]

        while syote not in mahdolliset_syotteet:
            syote = input(
                "Syötä joko pelattava kortti, nosta (N) uusi kortti tai passaa (P): ")
            syote = syote.capitalize()

        return syote

    def tulosta_pelaajan_kortit(self):
        """Tulostaa pelaajan kortit ja tallentaa ne dictionaryyn kortin
        valintaa varten.
        """
        pelaaja = self.get_vuorossaoleva_pelaaja()
        pelaaja.tulosta_kasi()
        pelaajan_kasi = {}

        for i, kortti in enumerate(pelaaja.get_kasi(), start=1):
            pelaajan_kasi[str(i)] = kortti

        return pelaajan_kasi

    def _nosta_kortti(self):
        pelaaja = self.get_vuorossaoleva_pelaaja()
        if self._hyvaksyta_nosto():
            pelaaja.nosta_kortti(self.nostopakka.jaa_kortti())
            print(f"Nostettu kortti: {pelaaja.get_viimeinen_kortti()}")

    def _hyvaksyta_nosto(self):
        """Metodi tarkastaa pelaajan oikeuden kortin nostoon.
        Pelaaja ei voi nostaa uutta kortia, jos jokin hänen
        kädessään olevista korteista on pelattavissa. Pelaaja
        ei voi myöskään nostaa yhtä korttia enempää vuoronsa
        aikana.
        """
        pelaaja = self.get_vuorossaoleva_pelaaja()
        kasi = pelaaja.get_kasi()

        for kortti in kasi:

            if self._hyvaksyta_pelattu_kortti(kortti, nosto=True):
                print((f"Et voi nostaa uutta korttia, koska kädessäsi oleva "
                       f"kortti {kortti} on pelattavissa."))
                return False

            if self.kortti_nostettu:
                print("Olet jo nostanut kortin!")
                return False

        self.kortti_nostettu = True
        return True

    def _passaa(self):
        if self.kortti_nostettu or len(self.nostopakka) == 0:
            self.vuoro_pelattu = True
        else:
            print("Et ole vielä nostanut korttia!")

    def _pelaa_kortti(self, kortti):
        """Metodi hoitaa pelattuun korttiin liittyvät toiminnot.
        """
        pelaaja = self.get_vuorossaoleva_pelaaja()
        if self._hyvaksyta_pelattu_kortti(kortti):

            if self.jokerivari != Config.ERIKOISVARI:
                self.jokerivari = Config.ERIKOISVARI

            if kortti.toiminta:

                if kortti.arvo != 11:
                    self.toimintakortin_pelannut_pelaaja = pelaaja

                self._kasittele_toimintakortti(kortti)

            pelaaja.pelaa_vuoro(kortti)
            self.poistopakka.lisaa_kortti(kortti)
            self.vuoro_pelattu = True

    def _hyvaksyta_pelattu_kortti(self, pelattu_kortti, nosto=False):
        """Tarkistaa, että onko pelaajan valitsema kortti pelattavissa.
        """
        return True  # TODO
        verrattava_kortti = self.poistopakka.get_viimeinen_kortti()

        if pelattu_kortti.vari == verrattava_kortti.vari or \
                pelattu_kortti.arvo == verrattava_kortti.arvo or \
                pelattu_kortti.vari == Config.ERIKOISVARI or \
                pelattu_kortti.vari == self.jokerivari:
            return True

        if not nosto:
            print("Kortti ei kelpaa!")

        return False

    def _kasittele_toimintakortti(self, pelattu_kortti):
        """Suorittaa toimintakorttiin liittyvät operaatiot.
        Toimintakortit määritellään niiden arvon perusteella.
        """
        # ohitus
        if pelattu_kortti.arvo == 10:
            self.seuraava_pelaaja()

        # suunnanvaihto
        elif pelattu_kortti.arvo == 11:
            self._vaihda_pelisuunta()

        # nosta 2
        elif pelattu_kortti.arvo == 12:
            seuraava_pelaaja = self.get_seuraava_pelaaja()

            for i in range(0, 2):
                seuraava_pelaaja.nosta_kortti(self.nostopakka.jaa_kortti())

            self.seuraava_pelaaja()

        elif pelattu_kortti.arvo == 13 or pelattu_kortti.arvo == 14:
            self._kasittele_jokerikortti(pelattu_kortti)

    def _kasittele_jokerikortti(self, pelattu_kortti):
        varit = self.nostopakka.get_varit()
        varivalinta = {str(i): vari for i, vari in enumerate(varit, start=1)}

        for i, vari in varivalinta.items():
            print(f"    {i:>2} - {vari}")

        syote = ""
        while syote not in varivalinta:
            syote = input("Mitä väriä kysytään? ")

        self.jokerivari = varivalinta[syote]

        if pelattu_kortti.arvo == 14:
            seuraava_pelaaja = self.get_seuraava_pelaaja()

            for _ in range(0, 4):
                seuraava_pelaaja.nosta_kortti(self.nostopakka.jaa_kortti())

            self.seuraava_pelaaja()

    def _vaihda_pelisuunta(self):
        self.pelisuunta *= -1

    def _tarkista_voitto(self):
        """Tarkistaa, että jääkö vuoron pelanneen pelaajan käteen
        kortteja. Jos käsi on tyhjä, pelaaja voittaa."""
        if not self.toimintakortin_pelannut_pelaaja:
            pelaaja = self.get_vuorossaoleva_pelaaja()
        else:
            pelaaja = self.toimintakortin_pelannut_pelaaja

        if len(pelaaja.get_kasi()) == 0:
            pelaaja.voittaa()
            return True
        else:
            return False

    def _laske_voittopisteet(self):
        voittaja = self.get_vuorossaoleva_pelaaja()
        for pelaaja in self.pelaajat:
            for kortti in pelaaja.get_kasi():
                voittaja.lisaa_pisteita(kortti.get_pisteet())

    def _tarkista_voittopisteet(self):
        """Tarkistaa, onko jokin pelaajista saavuttanut voittoon
        tarvittavat pisteet."""
        for pelaaja in self.pelaajat:

            if pelaaja.get_pisteet() >= self.voittopisteet:
                print(f"Pelin voitti {pelaaja.get_nimi()}.")
                print(f"Kierroksia pelattiin yhteensä {self.kierros}.")
                print("Pistetilanne:")

                for pelaaja2 in self.pelaajat:
                    print(f"{pelaaja2.get_nimi()} - {pelaaja2.get_pisteet()}")

                return True
            return False
