import requests
import pandas as pd

BASE = 'https://fantasy.premierleague.com/api/'


def gameweek_live(gameweek_id) -> dict:
    """
    :param gameweek_id:
    :return:
    """
    return requests.get(BASE + f'event/{gameweek_id}/live/').json()


def manager_info(manager_id) -> dict:
    """
    :param manager_id:
    :return:
    """
    return requests.get(BASE + f'entry/{manager_id}/').json()


def manager_history(manager_id) -> dict:
    """
    :param manager_id:
    :return:
    """
    return requests.get(BASE + f'entry/{manager_id}/history').json()


def league_standings(league_id) -> dict:
    """
    :param league_id:
    :return:
    """
    return requests.get(BASE + f'leagues-classic/{league_id}/standings').json()


def manager_teams(manager_id, event_id) -> dict:
    """
    :param manager_id:
    :param event_id:
    :return:
    """
    return requests.get(BASE + f'entry/{manager_id}/event/{event_id}/picks/').json()


def dream_team(event_id) -> dict:
    """
    :param event_id:
    :return:
    """
    return requests.get(BASE + f'dream-team/{event_id}/').json()


def set_piece() -> dict:
    """
    :return:
    """
    return requests.get(BASE + f'team/set-piece-notes/').json()


class FPLClient:
    BASE = 'https://fantasy.premierleague.com/api/'
    ENDPOINTS = {
        '_General': 'bootstrap-static/',
        '_Fixtures': 'fixtures/',
        '_EventStatus': 'event-status/',
        '_PlayerDetails': 'element-summary/%s/',  # Player's ID
        '_GameWeekLive':'event/%s/live/',  # GameWeek's ID
        '_ManagerInfo':'entry/%s/',  # Manager's ID
        '_ManagerHistory': 'entry/%s/history',  # Manager's ID
        '_LeagueStandings': 'leagues-classic/%s/standings',  # League's ID
        '_ManagerTeams': 'entry/%s/event/%d/picks/',  # Manager's ID, GameWeek's ID
        '_DreamTeam': 'dream-team/%s/',  # GameWeek's ID
        '_SetPiece': 'team/set-piece-notes/',
    }

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
