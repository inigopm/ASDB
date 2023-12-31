# -*- coding: utf-8 -*-
"""trusted_zone_javi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YtEHs05kAVI8QythbvbFTi3zSmUV5tIU

# Trusted zone
"""

import duckdb
import pandas as pd
import numpy as np
import os
import re

from pathlib import Path

FORMATTED_DIR = "formatted/laciudadaldia/"
TRUSTED_DIR = "trusted/laciudadaldia.parquet"
DATASET_NAME = "laciudadaldia"

con = duckdb.connect()

formatted_paths = [
    Path(FORMATTED_DIR + file_name)
    for file_name in os.listdir(FORMATTED_DIR)
]

latest_file = sorted(formatted_paths)[-1]

df = pd.read_parquet(latest_file)
df

"""
# Check the shape, columns, and data types of the DataFrame


"""

df.shape

df.columns

df.dtypes

df = df.astype({"data_indicador": "string"})

df.dtypes

"""# Check for missing values and duplicates in the DataFrame"""

df.isnull().sum()

df.duplicated().sum()

"""# Check the summary statistics of the numerical columns"""

df.describe()

"""# Check the distribution and outliers of the numerical columns using histograms"""

df.hist()

"""# Assert data quality"""

wrong_date_format = (
    df
    .data_indicador
    .apply(lambda x: bool(re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", x)))
    .all()
    )

assert wrong_date_format, "There are date values with wrong format"

date_is_primary_key = (
    df
    .data_indicador
    .value_counts()
    .eq(1)
    .all()
    )
assert date_is_primary_key, "There are repeated date values"

price_columns = [
    "electricity_price",
    "fish_and_seafood_price",
    "fuel_price",
    "meat_and_fish_price",
    "meat_price",
    "ibex_35",
]

exists_negative_prices = (
    df
    [price_columns]
    .lt(0)
    .any(axis=None)

)

assert not exists_negative_prices, "There are negative prices"

percentage_columns = [
    "credit_card_usage",
    "hotel_bookings_domestic",
    "hotel_bookings_international",
]

exists_extreme_percentages = (
    df
    [percentage_columns]
    .apply(lambda col: np.logical_and(
        col.lt(-200),
        col.gt(200))
    )
    .any(axis=None)
)

assert not exists_extreme_percentages, "There are extremely large percentages"

df.describe()

"""# Update dataset"""

try:
  old_df = pd.read_parquet(TRUSTED_DIR)
except FileNotFoundError:
  old_df = df

con.register("new_data", df)
con.register("old_data", old_df)


con.execute(f"create or replace table {DATASET_NAME}_new as select * from new_data")
con.execute(f"create or replace table {DATASET_NAME} as select * from old_data")

update_query = f"""
select
  coalesce(new.data_indicador, old.data_indicador) data_indicador,
  coalesce(new.credit_card_usage, old.credit_card_usage) credit_card_usage,
  coalesce(new.electricity_price, old.electricity_price) electricity_price,
  coalesce(new.fish_and_seafood_price, old.fish_and_seafood_price) fish_and_seafood_price,
  coalesce(new.fuel_price, old.fuel_price) fuel_price,
  coalesce(new.hotel_bookings_domestic, old.hotel_bookings_domestic) hotel_bookings_domestic,
  coalesce(new.hotel_bookings_international, old.hotel_bookings_international) hotel_bookings_international,
  coalesce(new.ibex_35, old.ibex_35) ibex_35,
  coalesce(new.meat_and_fish_price, old.meat_and_fish_price) meat_and_fish_price,
  coalesce(new.meat_price, old.meat_price) meat_price
from
  {DATASET_NAME} old
  full outer join {DATASET_NAME}_new new
    on old.data_indicador = new.data_indicador
"""
con.execute(f"create or replace table {DATASET_NAME} as {update_query}")

updated_table = con.execute(f"select * from {DATASET_NAME}").df()
updated_table

updated_table.to_parquet(TRUSTED_DIR)

con.close()