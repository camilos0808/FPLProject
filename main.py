import api as client
import pandas as pd

def get_player():
    client.general_info()

def get_fixtures_info():
    return

response = client.general_info()
print(response.keys())
df = pd.DataFrame(response['events'])

response2 = client.gameweek_live(13)
df2 = pd.DataFrame(response2['elements'])

info = client.general_info()