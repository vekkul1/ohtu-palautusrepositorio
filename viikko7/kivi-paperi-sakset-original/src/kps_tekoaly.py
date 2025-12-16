from tekoaly import Tekoaly
from templates.kps import KiviPaperiSakset


class KPSTekoaly(KiviPaperiSakset):
    def __init__ (self):
        self._tekoaly = Tekoaly()
    
    def _toisen_siirto(self, ekan_siirto):
        valinta = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {valinta}")

        return valinta
