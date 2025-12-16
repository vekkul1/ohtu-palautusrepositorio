
# Luokka pitää kirjaa ensimmäisen ja toisen pelaajan pisteistä sekä tasapelien määrästä.
class Tuomari:
    def __init__(self):
        self.ekan_pisteet = 0
        self.tokan_pisteet = 0
        self.tasapelit = 0

    def kirjaa_siirto(self, ekan_siirto, tokan_siirto):
        if self._tasapeli(ekan_siirto, tokan_siirto):
            self.tasapelit = self.tasapelit + 1
        elif self._eka_voittaa(ekan_siirto, tokan_siirto):
            self.ekan_pisteet = self.ekan_pisteet + 1
        else:
            self.tokan_pisteet = self.tokan_pisteet + 1

    def __str__(self):
        return f"Pelitilanne: {self.ekan_pisteet} - {self.tokan_pisteet}\nTasapelit: {self.tasapelit}"

    # sisäinen metodi, jolla tarkastetaan tuliko tasapeli
    def _tasapeli(self, eka, toka):
        if eka == toka:
            return True

        return False

    # sisäinen metodi joka tarkastaa voittaako eka pelaaja tokan
    def _eka_voittaa(self, eka, toka):
        if eka == "k" and toka == "s":
            return True
        elif eka == "s" and toka == "p":
            return True
        elif eka == "p" and toka == "k":
            return True

        return False

    def tulos(self, eka, toka):
        """Return 'eka' if first player won the round, 'toka' if second player won, 'tasapeli' if tie."""
        if self._tasapeli(eka, toka):
            return 'tasapeli'
        if self._eka_voittaa(eka, toka):
            return 'eka'
        return 'toka'

    def voittaja(self, tavoite=5):
        """Return 'eka' if first player has reached target points, 'toka' if second player, otherwise None."""
        if self.ekan_pisteet >= tavoite:
            return 'eka'
        if self.tokan_pisteet >= tavoite:
            return 'toka'
        return None

    def onko_peli_loppu(self, tavoite=5):
        return self.voittaja(tavoite) is not None
