import FPLClient as client
import posgress.connect.connect as connect
import pandas as pd


def connection(func):
    def wrapper(self, *args, **kwargs):
        self.conn = connect.connect()
        self.cur = self.conn.cursor()
        result = func(self, *args, **kwargs)
        self.cur.close()
        self.conn.close()
        return result

    return wrapper


def parse_fixture(fixtures: list):
    fix_parsed = [{x: fixtures[i][x] for x in fixtures[i] if x not in ['stats']} for i in
                  range(0, len(fixtures))]  # Remove Stats
    fix_parsed = [tuple(i.values()) for i in fix_parsed]

    return fix_parsed


class DataPusher:
    def __int__(self):
        self.conn = None
        self.cur = None

    @connection
    def update_fixture(self, fixtures: list):
        """

        :param fixtures:
        :return:
        """
        try:
            self.cur.execute("SET SCHEMA 'fpl';")
            self.cur.execute('BEGIN')
            self.cur.execute("TRUNCATE fixtures")
            self.cur.executemany("insert into fixtures values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 fixtures)
            self.conn.commit()
            return_value = self.cur.fetchall()
        except Exception as e:
            if e.__str__() != 'no results to fetch':
                self.conn.rollback()
                print(e.__str__())
            return_value = e

        return return_value

    @connection

client = client.FPLClient()
pusher = DataPusher()

fix = client.fixtures.all()
parsed = parse_fixture(fix)

fetch = pusher.update_fixture(parsed)
