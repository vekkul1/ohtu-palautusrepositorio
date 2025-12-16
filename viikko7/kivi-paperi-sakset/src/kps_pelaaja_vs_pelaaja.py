from templates.kps import KiviPaperiSakset


class KPSPelaajaVsPelaaja(KiviPaperiSakset):
    def _toisen_siirto(self, ekan_siirto):
        return input("Toisen pelaajan siirto: ")
