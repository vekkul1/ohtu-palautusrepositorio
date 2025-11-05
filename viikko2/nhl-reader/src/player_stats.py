
class PlayerStats:
    def __init__(self, reader):
        self.reader = reader
        self.players = self.reader.get_players()
    def nationality(self, country):
        players = []
        for p in self.players:
            if p.nationality == country.upper():
                players.append(p)
        return sorted(players, key=lambda p: p.points, reverse=True)
    def get_nationalities(self):
        nationalities = []
        for p in self.players:
            if p.nationality not in nationalities:
                nationalities.append(p.nationality)
        return sorted(nationalities)
