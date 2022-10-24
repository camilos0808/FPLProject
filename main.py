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


# pprint.pp(df.loc[15, 'stats'])

def get_all_players():
    df_all = pd.DataFrame()
    for player_id in players['id'].tolist():
        a = client.details.all(player_id)
        df_p = pd.DataFrame(a['history'])
        if df_all.__len__() == 0:
            df_all = df_p
        else:
            df_all = pd.concat([df_all, df_p])
    return df_all


# df_all = get_all_players()
# df_all['opponent_team'] = df_all['opponent_team'].apply(get_team)
# df_all['element'] = df_all['element'].apply(get_player)


b = client.fixtures.get_table(14)
b['team'] = b['team'].apply(get_team)
