from templates.kps import KiviPaperiSakset
from tekoaly_parannettu import TekoalyParannettu


class KPSParempiTekoaly(KiviPaperiSakset):
    def __init__ (self):
        self._tekoaly = TekoalyParannettu(10)
    
    def _toisen_siirto(self, ekan_siirto):
        valinta = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {valinta}")
        self._tekoaly.aseta_siirto(ekan_siirto)
        return valinta