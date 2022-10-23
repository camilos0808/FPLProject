import api as client
import pandas as pd
import pprint
import requests

client = client.FPLClient()

teams = client.general.teams_details()
players = client.general.players_details()


def get_team(id):
    return teams.set_index('id').loc[id, 'name']


def get_player(id):
    return players.set_index('id').loc[id, 'web_name']


df = client.fixtures.all()
df = pd.DataFrame(df)
df['team_a'] = df['team_a'].apply(get_team)
df['team_h'] = df['team_h'].apply(get_team)

pprint.pp(df.loc[15, 'stats'])
