from enum import Enum

class SortBy(Enum):
    POINTS = lambda player: player.points
    GOALS = lambda player: player.goals
    ASSISTS = lambda player: player.assists


class StatisticsService:
    def __init__(self, player_reader):
        reader = player_reader

        self._players = reader.get_players()

    def search(self, name):
        for player in self._players:
            if name in player.name:
                return player

        return None

    def team(self, team_name):
        players_of_team = filter(
            lambda player: player.team == team_name,
            self._players
        )

        return list(players_of_team)

    def top(self, how_many, sortBy = SortBy.POINTS):
        # metodin käyttämä apufufunktio voidaan määritellä näin

        sorted_players = sorted(
            self._players,
            reverse=True,
            key=sortBy
        )

        result = []
        i = 0
        while i < how_many:
            result.append(sorted_players[i])
            i += 1

        return result
