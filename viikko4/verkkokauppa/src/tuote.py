class Tuote:
    def __init__(self, id, nimi, hinta, important = False):
        self.id = id
        self.nimi = nimi
        self.hinta = hinta
        self.important = important

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.nimi
    
    def toggle_important(self):
        self.important = !self.important
