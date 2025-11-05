import requests
from rich.table import Table
from player import Player

class PlayerReader:
    def __init__ (self, url):
        self.url = url
    def get_players(self):
        response = requests.get(self.url, timeout=10).json()
        def dict_to_player(player):
            return Player(player)
        return list(map(dict_to_player, response))
    def players_to_table(self, players, years):
        title = f"Season {years} players from {players[0].nationality}"
        table = Table(title=title, show_header = True, header_style="bold")
        table.add_column("Released", width=22, style="cyan")
        table.add_column("Team", max_width=15, style="magenta")
        table.add_column("Goals", style="green", justify="right")
        table.add_column("Assists", style="green", justify="right")
        table.add_column("Points", style="green", justify="right")
        for p in players:
            table.add_row(
                str(p.name),
                str(p.team),
                str(p.goals),
                str(p.assists),
                str(p.points)
            )
        return table
