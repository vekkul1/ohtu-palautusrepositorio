from rich.console import Console
from player_reader import PlayerReader
from player_stats import PlayerStats
#from player_to_table import player_to_table

def main():
    console = Console()
    season = console.input("Season [bright blue] (2024-25) [/]")
    url=f"https://studies.cs.helsinki.fi/nhlstats/{season if season else "2024-25"}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    while True:
        country = input(f"Nationality [{"/".join(stats.get_nationalities())}] ")

        if country.upper() in stats.get_nationalities():
            console.print(reader.players_to_table(stats.nationality(country), season))
        else:
            return

if __name__ == "__main__":
    main()
