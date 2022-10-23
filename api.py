import requests
import pandas as pd
from _endpoints import ENDPOINTS


class FPLClient:
    BASE = 'https://fantasy.premierleague.com/api/'
    ENDPOINTS = ENDPOINTS

    def __init__(self):
        for key in FPLClient.ENDPOINTS.keys():
            cls = eval('self.' + key)
            setattr(self, cls.ATR_NAME, cls())

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

    class _General(__Endpoint):

        ATR_NAME = 'general'

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

    class _Fixtures(__Endpoint):
        ATR_NAME = 'fixtures'

    class _EventStatus(__Endpoint):
        ATR_NAME = 'event_status'

    class _PlayerDetails(__Endpoint):
        ATR_NAME = 'players_details'

    class _GameWeekLive(__Endpoint):
        ATR_NAME = 'week_live'

    class _ManagerInfo(__Endpoint):
        ATR_NAME = 'manager_info'

    class _ManagerHistory(__Endpoint):
        ATR_NAME = 'manager_history'

    class _LeagueStandings(__Endpoint):
        ATR_NAME = 'league_standings'

    class _ManagerTeams(__Endpoint):
        ATR_NAME = 'manager_teams'

    class _DreamTeam(__Endpoint):
        ATR_NAME = 'dream_team'

    class _SetPiece(__Endpoint):
        ATR_NAME = 'set_piece'


client = FPLClient()
