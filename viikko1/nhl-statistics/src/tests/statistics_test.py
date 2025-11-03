import unittest 
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        #self.stub = PlayerReaderStub()
    
    def test_search_finds_correct_player(self): 
        search = self.stats.search("Kurri")

        self.assertEqual(search.name, "Kurri")

    def test_search_with_wrong_name(self):
        search = self.stats.search("Pentti")

        self.assertEqual(search, None)

    def test_team_search(self):
        team = self.stats.team("PIT")

        self.assertEqual(team[0].name, "Lemieux")
        
    def test_team_search_with_wrong_team(self):
        team = self.stats.team("HIFK")

        self.assertEqual(team, [])

    def test_top_returns_right_amount_of_people(self):
        top = self.stats.top(2)

        self.assertEqual(len(top), 2)

    def test_top_returns_right_top_scorer(self):
        top = self.stats.top(1)

        self.assertEqual(top[0].name, "Gretzky")

    def test_top_sortby_goals(self):
        top = self.stats.top(1, SortBy.GOALS)

        self.assertEqual(top[0].name, "Lemieux")

    def test_top_sortby_assists(self):
        top = self.stats.top(1, SortBy.ASSISTS)

        self.assertEqual(top[0].name, "Gretzky")