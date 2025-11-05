class Player:
    def __init__(self, dictionary):
        self.name = dictionary["name"]
        self.nationality = dictionary["nationality"]
        self.team = dictionary["team"]
        self.goals = dictionary["goals"]
        self.assists = dictionary["assists"]
        self.points = self.goals+self.assists
    def __str__(self):
        name_team=f"{self.name:22} {self.team:15}"
        points = f"{self.goals:2} + {self.assists:2} = {self.points:2}"
        return f"{name_team} {points}"
