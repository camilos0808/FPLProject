import FPLClient as client
import pandas as pd

client = client.FPLClient()
general = client.general.all()
teamdetails = client.general.teams_details()
gameweek = client.general.gameweek_details()
players = client.general.players_details()
fixtures = client.fixtures.all()
stats = client.general.player_stats_list()