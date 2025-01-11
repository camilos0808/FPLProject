import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def to_parquet(table: pd.DataFrame(), filename: str):
    table = pa.Table.from_pandas(table)
    pq.write_table(table, 'parquet/{}.parquet'.format(filename))


def from_parquet(filename: str) -> pd.DataFrame():
    return pd.read_parquet('parquet/{}.parquet'.format(filename), engine='pyarrow')