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


# df = client.fixtures.all()
# df = pd.DataFrame(df)
# df['team_a'] = df['team_a'].apply(get_team)
# df['team_h'] = df['team_h'].apply(get_team)


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


# b = client.fixtures.get_table(14)
# b['team'] = b['team'].apply(get_team)

df_ = get_all_players()
df = df_.copy()

all_fixtures = pd.DataFrame(client.fixtures.all())

df = df.join(all_fixtures[['id', 'event']].set_index('id'), on='fixture')

table_df = pd.DataFrame()
_list = df.event.unique()
_list.sort()
for _ in _list:
    table_wdf = client.fixtures.get_table(_)
    table_wdf['event'] = _
    if table_df.__len__() == 0:
        table_df = table_wdf
    else:
        table_df = pd.concat([table_df, table_wdf])

table_df.reset_index(inplace=True)
table_df['index'] += 1
table_df.columns = ['position_oppo', 'opponent_team', 'points', 'favor', 'against', 'diff', 'event']
df = pd.merge(df, table_df[['position_oppo', 'opponent_team', 'event']], how='left',
              left_on=['opponent_team', 'event'],
              right_on=['opponent_team', 'event'])

fix_merge = all_fixtures[['team_h', 'team_a', 'event']].copy()
dfOppoVisit = df.loc[df['was_home']].copy()
fix_merge.columns = ['team', 'opponent_team', 'event']
dfOppoVisit = pd.merge(dfOppoVisit, fix_merge, how='left',
                       left_on=['opponent_team', 'event'],
                       right_on=['opponent_team', 'event'])

dfOppoHome = df.loc[~df['was_home']].copy()
fix_merge.columns = ['opponent_team', 'team', 'event']
dfOppoHome = pd.merge(dfOppoHome, fix_merge, how='left',
                      left_on=['opponent_team', 'event'],
                      right_on=['opponent_team', 'event'])

df = pd.concat([dfOppoVisit, dfOppoHome], ignore_index=True)

a = 5
# todo Clima
# todo

