import random

from config import Config
from pakka import Pakka
from pelaaja import Pelaaja
from feed import Feed


class Peli:
    """Tämä luokka pitää sisällään UNO-korttipelin logiikan.
    Peli-olion saa helposti luotua oletusasetuksilla kutsumalla
    Peli.palauta_perus_peli()-metodin. Oletuksena on 3 pelaajaa ja
    voittoon tarvitaan 500 pistettä.

    :param: pelaajien_lkm: Pelaajien lukumäärä
    :param: voittopisteet: Voittoon tarvittavien pisteiden määrä
    """

    def __init__(self):
        self.pelaajat = []
        self.nostopakka = Pakka()
        self.poistopakka = Pakka()
        self.varit = Config.KORTTIVARIT
        self.jokerivari = Config.ERIKOISVARI
        self.feed = Feed(50)

        self._alusta_pelimuuttujat()

    def _alusta_pelimuuttujat(self):
        self.kierros = 1
        self.vuorossa = 0
        self.aloittaja = 0
        self.pelisuunta = 1
        self.kortti_nostettu = False
        self.kortti_nostettu_tietokone = False
        self.vuoro_pelattu = False
        self.vuoro_pelattu_tietokone = False
        self.kierros_pelattu = False
        self.peli_pelattu = False
        self.ohitus = False
        self.kysytaan_varia = False

        # Muuttujaa käytetään pelaajan voiton määrityksessä.
        # Jos pelaajan viimeinen kädessä oleva kortti on
        # toimintakortti, niin kun se pelataan, saattaa vuorossa
        # oleva pelaaja vaihtua. Tässä tapauksessa ilman tätä
        # apumuuttujaa voitontarkistus ei toimi oikein.
        # TODO Ehkä turha muuttuja.
        self.toimintakortin_pelannut_pelaaja = None

    @classmethod
    def palauta_peruspeli(cls):
        """3 pelaajaa ja voittoon varvittavat pisteet 500
        """
        return cls(3, 500)

    @classmethod
    def palauta_testipeli(cls):
        """Testaamiseen tarkoitettu pelinluontimetodi.
        """
        return cls(2, 50)

    def luo_pelaaja(self, nimi, tietokone):
        self.pelaajat.append(Pelaaja(nimi, tietokone))

    def aloita_ensimmainen_peli(self):
        self.pelaajien_lkm = len(self.pelaajat)
        self.voittopisteet = Config.VOITTOPISTEET
        self.pelaa_peli()

    def aloita_uusi_peli(self):
        for pelaaja in self.pelaajat:
            pelaaja.resetoi()
        self._alusta_pelimuuttujat()
        self.pelaa_peli()

    def pelaa_peli(self):
        tilanne = "peli" if self.kierros == 1 else "kierros"
        self.feed.add_msg(
            f"Uusi {tilanne} alkaa. Kierroksen numero on {self.kierros}.")
        self.kierros_pelattu = False
        self.nostopakka.luo_pakka()
        self.nostopakka.sekoita()
        self._jaa_aloituskortit()
        self.nostopakka.kaanna_pakka()
        self._aloituskortti_poistopakkaan()
        if self.kierros > 1:
            self._maarita_aloittava_pelaaja()

        self.toimintakortin_pelannut_pelaaja = None

        if self.vuorossa != 0:
            self._pelaa_tietokoneiden_vuorot()

    def _maarita_aloittava_pelaaja(self):
        if self.aloittaja < self.pelaajien_lkm - 1:
            self.aloittaja += 1
            self.vuorossa = self.aloittaja
        else:
            self.aloittaja, self.vuorossa = 0, 0

    def _get_vuorossaoleva_pelaaja(self):
        return self.pelaajat[self.vuorossa]

    def _get_seuraava_pelaaja(self):
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

    def _seuraava_pelaaja(self):
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

    def _jaa_aloituskortit(self):
        """Jaetaan aloituskortit kaikille pelissä oleville
        pelaajille."""
        for _ in range(0, 7):
            for pelaaja in self.pelaajat:
                pelaaja.nosta_kortti(self.nostopakka.jaa_kortti())
        for pelaaja in self.pelaajat:
            pelaaja.kasi.sort()

    def _aloituskortti_poistopakkaan(self):
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

    def _tuhoa_pelaajien_kadet(self):
        """Jokaisen kierroksen päätyttyä pelaajien
        kädet nollataan."""
        for pelaaja in self.pelaajat:
            pelaaja.tuhoa_kasi()

    def pelaa_kortti(self, kortti):
        """Tata metodia kutsutaan tiedostosta ui.py. Kun pelaaja valitsee
        kortin klikkaamalla sitä, kutsutaan tämä metodi.
        """
        self.vuoro_pelattu_tietokone = False
        pelaaja = self._get_vuorossaoleva_pelaaja()
        kortti = pelaaja.get_kasi()[kortti]
        self._pelaa_kortti(kortti)

        if self.kysytaan_varia:
            pass

        self._suorita_voiton_tarkistus(pelaaja)
        if self.kierros_pelattu:
            return

        if self.vuoro_pelattu:
            self._siirra_vuoro_tietokoneelle()

    def nosta_kortti(self):
        self._nosta_kortti()

    def passaa(self):
        self.vuoro_pelattu_tietokone = False
        self._passaa()

        if self.vuoro_pelattu:
            self._siirra_vuoro_tietokoneelle()

    def ohita_pelaajan_vuoro(self):
        self.vuoro_pelattu_tietokone = False
        self.ohitus = False
        self.feed.add_msg(f"Pelaajan 1 vuoro ohitetaan.")
        self._siirra_vuoro_tietokoneelle()

    def vastaanota_vari(self, vari):
        # kutsutaan guista
        self.kysytaan_varia = False
        self.vuoro_pelattu = True
        self.jokerivari = vari
        self.feed.add_msg(f"Jokerivari on {vari}.")
        self._siirra_vuoro_tietokoneelle()

    # TODO poista tama metodi
    # def _alusta_vuoro(self):
    #     self.vuoro_pelattu_tietokone = False

    #     kysyttava_kortti = self.poistopakka.get_viimeinen_kortti()
    #     print(f"Pelaajalta kysyttyva kortti on {kysyttava_kortti}.")

    #     if kysyttava_kortti.arvo >= 13:
    #         print(f"Jokeriväri on {self.jokerivari}.")

    #     pelaaja = self._get_vuorossaoleva_pelaaja()
    #     print(f"Vuorossa on {pelaaja.get_nimi()}.")

    def _siirra_vuoro_tietokoneelle(self):
        self._seuraava_pelaaja()
        self._pelaa_tietokoneiden_vuorot()

    def _lopeta_vuoro(self, pelaaja):
        self.kortti_nostettu_tietokone = False
        self.vuoro_pelattu_tietokone = False
        voittaja = self._suorita_voiton_tarkistus(pelaaja)
        self._seuraava_pelaaja()
        return voittaja

    def _pelaa_tietokoneiden_vuorot(self):
        kysyttava_kortti = self.poistopakka.get_viimeinen_kortti()  # TODO
        print(f"Tietokoneelta kysyttyva kortti on {kysyttava_kortti}.")  # TODO

        # pelaavat_tietokoneet = [
        #     tietokone for tietokone in self.pelaajat[self.vuorossa:] if tietokone.tietokone]

        # for pelaaja in pelaavat_tietokoneet:
        while self.vuorossa != 0:
            pelaaja = self._get_vuorossaoleva_pelaaja()
            if self.ohitus:
                self._seuraava_pelaaja()
                self.ohitus = False
                self.feed.add_msg(
                    f"Pelaajan {pelaaja.get_nimi()} vuoro ohitetaan.")
                print(f"Pelaajan {pelaaja.get_nimi()} vuoro ohitetaan")
                continue
            print("vuorossa: {}".format(self.vuorossa))  # TODO
            kasi = pelaaja.get_kasi()
            random.shuffle(kasi)
            self._nosta_kortti()
            for kortti in kasi:
                print(kortti)  # TODO
                self._pelaa_kortti(kortti)
                if self.kysytaan_varia:
                    self.jokerivari = random.choice(self.varit)
                    self.feed.add_msg(f"Jokerivari on {self.jokerivari}.")
                    self.kysytaan_varia = False
                if self.vuoro_pelattu_tietokone:
                    break
            else:
                self._passaa()

            print("Tietokoneen vuoro pelattu")  # TODO testaus
            print(pelaaja.get_kasi())
            print("===========")
            voittaja = self._lopeta_vuoro(pelaaja)
            if voittaja:
                break

        self.vuoro_pelattu_tietokone = True
        self.vuoro_pelattu = False
        self.kortti_nostettu = False

    def _suorita_voiton_tarkistus(self, pelaaja):
        if self._tarkista_voitto(pelaaja):
            self._laske_voittopisteet()
            print(
                f"{self.kierros:>2}. kierroksen voittaja on {pelaaja.get_nimi()}. Pisteet: {pelaaja.get_pisteet()}.")
            self._tuhoa_pelaajien_kadet()
            self.feed.add_msg(
                f"Kierros {self.kierros} päättyi. Voittaja on {pelaaja.get_nimi()}.")
            self.kierros += 1
            self.kierros_pelattu = True

            if self._tarkista_voittopisteet():
                self.peli_pelattu = True

            return pelaaja

    def _pelaajan_syote(self):
        syote = ""
        mahdolliset_syotteet = [str(x) for x in range(
            1, len(self._get_vuorossaoleva_pelaaja().get_kasi()) + 1)] + ["N", "P"]

        while syote not in mahdolliset_syotteet:
            syote = input(
                "Syötä joko pelattava kortti, nosta (N) uusi kortti tai passaa (P): ")
            syote = syote.capitalize()

        return syote

    def tulosta_pelaajan_kortit(self):
        """Tulostaa pelaajan kortit ja tallentaa ne dictionaryyn kortin
        valintaa varten.
        """
        pelaaja = self._get_vuorossaoleva_pelaaja()
        pelaaja.tulosta_kasi()
        pelaajan_kasi = {}

        for i, kortti in enumerate(pelaaja.get_kasi(), start=1):
            pelaajan_kasi[str(i)] = kortti

        return pelaajan_kasi

    def _nosta_kortti(self):
        pelaaja = self._get_vuorossaoleva_pelaaja()
        if self._hyvaksyta_nosto():
            if pelaaja.tietokone:
                print("Tietokone nostaa kortin")
            pelaaja.nosta_kortti(self.nostopakka.jaa_kortti())
            print(f"Nostettu kortti: {pelaaja.get_viimeinen_kortti()}")
            if not pelaaja.tietokone:
                pelaaja.kasi.sort()

    def _hyvaksyta_nosto(self):
        """Metodi tarkastaa pelaajan oikeuden kortin nostoon.
        Pelaaja ei voi nostaa uutta kortia, jos jokin hänen
        kädessään olevista korteista on pelattavissa. Pelaaja
        ei voi myöskään nostaa yhtä korttia enempää vuoronsa
        aikana.
        """
        pelaaja = self._get_vuorossaoleva_pelaaja()
        kasi = pelaaja.get_kasi()

        for kortti in kasi:

            if self._hyvaksyta_pelattu_kortti(kortti, nosto=True):
                print((f"Et voi nostaa uutta korttia, koska kädessäsi oleva "
                       f"kortti {kortti} on pelattavissa."))
                return False

        if self.kortti_nostettu and not pelaaja.tietokone:
            print("Olet jo nostanut kortin!")
            return False

        if self.kortti_nostettu_tietokone and pelaaja.tietokone:
            return False

        self.feed.add_msg(f"{pelaaja.get_nimi()} nostaa kortin.")

        self.kortti_nostettu = True
        if pelaaja.tietokone:
            self.kortti_nostettu_tietokone = True
        return True

    def _passaa(self):
        pelaaja = self._get_vuorossaoleva_pelaaja()
        if self.kortti_nostettu or len(self.nostopakka) == 0:
            self.feed.add_msg(f"{pelaaja.get_nimi()} passaa.")
            self.vuoro_pelattu = True
        else:
            print("Et voi passata!")
        if pelaaja.tietokone and (self.kortti_nostettu_tietokone or len(self.nostopakka) == 0):
            self.vuoro_pelattu_tietokone = True

    def _pelaa_kortti(self, kortti):
        """Metodi hoitaa pelattuun korttiin liittyvät toiminnot.
        """
        pelaaja = self._get_vuorossaoleva_pelaaja()
        if self._hyvaksyta_pelattu_kortti(kortti):
            print(pelaaja.get_nimi(), kortti)  # TODO

            if self.jokerivari != Config.ERIKOISVARI:
                self.jokerivari = Config.ERIKOISVARI

            if kortti.toiminta:

                if kortti.arvo != 11:
                    self.toimintakortin_pelannut_pelaaja = pelaaja

                self._kasittele_toimintakortti(kortti)

            pelaaja.pelaa_vuoro(kortti)
            self.poistopakka.lisaa_kortti(kortti)
            
            if not self.kysytaan_varia:
                self.vuoro_pelattu = True

            self.feed.add_msg(f"{pelaaja.get_nimi()} pelasi kortin {kortti}.")

            if pelaaja.tietokone:
                print(f"Tietokone pelasi {kortti}")
                self.vuoro_pelattu_tietokone = True
            else:
                print(f"Pelaaja pelasi {kortti}")

    def _hyvaksyta_pelattu_kortti(self, pelattu_kortti, nosto=False):
        """Tarkistaa, että onko pelattu kortti valitsema kortti pelattavissa.
        """
        verrattava_kortti = self.poistopakka.get_viimeinen_kortti()

        # TODO tee tarkastusmetodit korttiluokkaan
        if (pelattu_kortti.vari == verrattava_kortti.vari or
            pelattu_kortti.arvo == verrattava_kortti.arvo or
            pelattu_kortti.vari == Config.ERIKOISVARI or
            pelattu_kortti.vari == self.jokerivari):
            return True

        return False

    def _kasittele_toimintakortti(self, pelattu_kortti):
        """Suorittaa toimintakorttiin liittyvät operaatiot.
        Toimintakortit määritellään niiden arvon perusteella.
        """
        # ohitus
        if pelattu_kortti.arvo == 10:
            self.ohitus = True
            # self._seuraava_pelaaja()  # TODO

        # suunnanvaihto
        elif pelattu_kortti.arvo == 11:
            self._vaihda_pelisuunta()

        # nosta 2
        elif pelattu_kortti.arvo == 12:
            self.ohitus = True  # TODO
            seuraava_pelaaja = self._get_seuraava_pelaaja()

            for i in range(0, 2):
                seuraava_pelaaja.nosta_kortti(self.nostopakka.jaa_kortti())

            # self._seuraava_pelaaja()  # TODO

        elif pelattu_kortti.arvo == 13 or pelattu_kortti.arvo == 14:
            self._kasittele_jokerikortti(pelattu_kortti)

    def _kasittele_jokerikortti(self, pelattu_kortti):
        self.kysytaan_varia = True
        # varivalinta = {str(i): vari for i, vari in enumerate(self.varit, start=1)}

        # for i, vari in varivalinta.items():
        #     print(f"    {i:>2} - {vari}")

        # syote = ""
        # while syote not in varivalinta:
        #     syote = input("Mitä väriä kysytään? ")

        # self.jokerivari = varivalinta[syote]

        if pelattu_kortti.arvo == 14:
            seuraava_pelaaja = self._get_seuraava_pelaaja()

            for _ in range(0, 4):
                seuraava_pelaaja.nosta_kortti(self.nostopakka.jaa_kortti())

            self._seuraava_pelaaja()

    # def _kasittele_jokerikortti(self, pelattu_kortti):
    #     varit = self.nostopakka.get_varit()
    #     varivalinta = {str(i): vari for i, vari in enumerate(varit, start=1)}

    #     for i, vari in varivalinta.items():
    #         print(f"    {i:>2} - {vari}")

    #     syote = ""
    #     while syote not in varivalinta:
    #         syote = input("Mitä väriä kysytään? ")

    #     self.jokerivari = varivalinta[syote]

    #     if pelattu_kortti.arvo == 14:
    #         seuraava_pelaaja = self._get_seuraava_pelaaja()

    #         for _ in range(0, 4):
    #             seuraava_pelaaja.nosta_kortti(self.nostopakka.jaa_kortti())

    #         self._seuraava_pelaaja()

    def _vaihda_pelisuunta(self):
        self.pelisuunta *= -1

    def _tarkista_voitto(self, pelaaja):
        """Tarkistaa, että jääkö vuoron pelanneen pelaajan käteen
        kortteja. Jos käsi on tyhjä, pelaaja voittaa."""
        if len(pelaaja.get_kasi()) == 0:
            pelaaja.voittaa()
            return True
        else:
            return False

    def _laske_voittopisteet(self):
        voittaja = self._get_vuorossaoleva_pelaaja()
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
