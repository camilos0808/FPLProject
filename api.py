import requests
import pandas as pd
from _endpoints import ENDPOINTS


class FPLClient:
    BASE = 'https://fantasy.premierleague.com/api/'
    ENDPOINTS = ENDPOINTS

    def __init__(self):
        self.general = eval('self.' + list(ENDPOINTS.keys())[0]+'()')
        self.fixtures = eval('self.' + list(ENDPOINTS.keys())[1]+'()')
        self.status = eval('self.' + list(ENDPOINTS.keys())[2]+'()')
        self.details = eval('self.' + list(ENDPOINTS.keys())[3]+'()')
        self.live = eval('self.' + list(ENDPOINTS.keys())[4]+'()')
        self.manager_info = eval('self.' + list(ENDPOINTS.keys())[5]+'()')
        self.manager_history = eval('self.' + list(ENDPOINTS.keys())[6]+'()')
        self.standings = eval('self.' + list(ENDPOINTS.keys())[7]+'()')
        self.manager_teams = eval('self.' + list(ENDPOINTS.keys())[8]+'()')
        self.dreamteam = eval('self.' + list(ENDPOINTS.keys())[9]+'()')
        self.setpiece = eval('self.' + list(ENDPOINTS.keys())[10]+'()')

    class _Endpoint:
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

    class _General(_Endpoint):

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

    class _Fixtures(_Endpoint):
        pass

    class _EventStatus(_Endpoint):
        pass

    class _PlayerDetails(_Endpoint):
        pass

    class _GameWeekLive(_Endpoint):
        pass

    class _ManagerInfo(_Endpoint):
        pass

    class _ManagerHistory(_Endpoint):
        pass

    class _LeagueStandings(_Endpoint):
        pass

    class _ManagerTeams(_Endpoint):
        pass

    class _DreamTeam(_Endpoint):
        pass

    class _SetPiece(_Endpoint):
        pass


client = FPLClient()
