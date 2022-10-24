import requests
import pandas as pd
from _endpoints import ENDPOINTS


class FPLClient:
    BASE = 'https://fantasy.premierleague.com/api/'
    ENDPOINTS = ENDPOINTS

    def __init__(self):
        self.general = self.__General()
        self.fixtures = self.__Fixtures()
        self.status = self.__EventStatus()
        self.details = self.__PlayerDetails()
        self.live = self.__GameWeekLive()
        self.manager_info = self.__ManagerInfo()
        self.manager_history = self.__ManagerHistory()
        self.standings = self.__LeagueStandings()
        self.manager_teams = self.__ManagerTeams()
        self.dreamteam = self.__DreamTeam()
        self.setpiece = self.__SetPiece()

    class __Endpoint:
        def __init__(self):
            self.ep = FPLClient.ENDPOINTS[self.__class__.__name__]

        def all(self, param=None) -> dict:
            """

            :param param:
            :return:
            """
            if param is None:
                return requests.get(FPLClient.BASE + self.ep).json()
            else:
                if isinstance(param, int):
                    param = [param]
                return requests.get(FPLClient.BASE + self.ep % tuple(param)).json()

    class __General(__Endpoint):

        def gameweek_details(self) -> pd.DataFrame:
            """
            :return:
            """
            return pd.DataFrame(self.all()['events'])

        def teams_details(self) -> pd.DataFrame:
            """
            :return:
            """
            return pd.DataFrame(self.all()['teams'])

        def players_details(self) -> pd.DataFrame:
            """
            :return:
            """
            return pd.DataFrame(self.all()['elements'])

        def player_stats_list(self) -> pd.DataFrame:
            """
            :return:
            """
            return pd.DataFrame(self.all()['element_stats'])

        def team_selection_details(self) -> pd.DataFrame:
            """

            :return:
            """
            return pd.DataFrame(self.all()['element_types'])

    class __Fixtures(__Endpoint):

        def get_table(self, week):
            b = pd.DataFrame(self.all())
            b = b.loc[(b['event'] < week) & ~(b['minutes'].isin([None, 0]))].copy()
            b['team_a_points'] = 0
            b['team_h_points'] = 0
            b.loc[(b['team_a_score'] > b['team_h_score']), 'team_a_points'] = 3
            b.loc[(b['team_a_score'] < b['team_h_score']), 'team_h_points'] = 3
            b.loc[(b['team_a_score'] == b['team_h_score']), ['team_a_points', 'team_h_points']] = 1

            home = b[['team_h', 'team_h_points', 'team_h_score', 'team_a_score']].copy()
            home.columns = ['team', 'points', 'favor', 'against']
            away = b[['team_a', 'team_a_points', 'team_a_score', 'team_h_score']].copy()
            away.columns = ['team', 'points', 'favor', 'against']
            tab = pd.concat([home, away])
            tab['diff'] = tab['favor'] - tab['against']
            tab = tab.groupby('team').sum().sort_values(['points', 'diff', 'favor', 'against'], ascending=False)
            return tab.reset_index()

    class __EventStatus(__Endpoint):
        pass

    class __PlayerDetails(__Endpoint):
        pass

    class __GameWeekLive(__Endpoint):
        pass

    class __ManagerInfo(__Endpoint):
        pass

    class __ManagerHistory(__Endpoint):
        pass

    class __LeagueStandings(__Endpoint):
        pass

    class __ManagerTeams(__Endpoint):
        pass

    class __DreamTeam(__Endpoint):
        pass

    class __SetPiece(__Endpoint):
        pass


client = FPLClient()
