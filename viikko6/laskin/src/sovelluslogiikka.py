class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvot = [arvo]
        self._index = 0

    def miinus(self, operandi):
        self._arvot.append(self._arvot[-1] - operandi)

    def plus(self, operandi):
        self._arvot.append(self._arvot[-1] + operandi)

    def nollaa(self):
        self._arvot.append(0)

    def aseta_arvo(self, arvo):
        self._arvot.append(arvo)

    def arvo(self):
        return self._arvot[-1]
    
    def kumoa(self):
        self._arvot.pop()

    def askel(self):
        return len(self._arvot)-1