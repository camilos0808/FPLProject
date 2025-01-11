from FPLClient import FPLClient
import pandas as pd
from parquet.dropper import from_parquet, to_parquet

client = FPLClient()

# Load Players Base Data
player_list = pd.DataFrame(client.general.all()['elements'])['id'].to_list()
dataset = pd.DataFrame()
for player in player_list:
    _player = pd.DataFrame(client.details.all(player)['history'])
    if dataset.__len__() == 0:
        dataset = _player
    else:
        dataset = pd.concat([dataset, _player], ignore_index=True)

# Remove not needed columns
dataset.drop(columns=['modified'], inplace=True)

# Save To Parquet
to_parquet(dataset, 'playersStats')

# Load Parquet Base File
dataset = from_parquet('playersStats')
