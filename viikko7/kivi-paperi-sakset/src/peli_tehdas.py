from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


class Peli:
    def _valitse_peli(self, tyyppi):
        if tyyppi == "a":
            return KPSPelaajaVsPelaaja()
        elif tyyppi == "b":
            return KPSTekoaly()
        elif tyyppi == "c":
            return KPSParempiTekoaly()
        else:
            return None
        
    def run(self):
        while True:
            print("Valitse pelataanko"
                "\n (a) Ihmistä vastaan"
                "\n (b) Tekoälyä vastaan"
                "\n (c) Parannettua tekoälyä vastaan"
                "\nMuilla valinnoilla lopetetaan"
            )
            tyyppi = input()
            if tyyppi not in ["a", "b", "c"]:
                break
            else:
                print(
                "Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s"
                )
                peli = self._valitse_peli(tyyppi)
                if peli:
                    peli.pelaa()