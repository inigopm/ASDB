# ADSDB_PATH= "C:/Users/inigo/Documents/UPC/ASDB/ASDB/"
FORMATTED_PATH = "formatted/articles/"
TRUSTED_PATH = "trusted/articles/"
METADATA_PATH = "metadata/"

import duckdb
import pandas as pd
import os
from pathlib import Path
import matplotlib.pyplot as plt

# Take most recent file
formatted_paths = [
    Path(FORMATTED_PATH + file_name)
    for file_name in os.listdir(FORMATTED_PATH)
]
latest_file = sorted(formatted_paths)[-1]

# Load file
df = pd.read_csv(latest_file)
df_big = pd.read_csv(os.path.join(TRUSTED_PATH, "articles.csv"))

# Remove unnecesary columns
df_filtered = df.drop(columns=['DATEADDED', 'SOURCEURL', 'MonthYear', 'Year', 'FractionDate'])

# Set the column "SQLDATE to a datetime object
df_filtered['SQLDATE'] = pd.to_datetime(df_filtered['SQLDATE'], format='%Y%m%d')
df_filtered['SQLDATE'] = df_filtered['SQLDATE'].dt.strftime('%Y-%m-%d')

# Filter er country and take only the articles related to Spain.
condition1 = df_filtered['Actor1Geo_CountryCode'].str.contains('SP', na=False)
condition2 = df_filtered['Actor2Geo_CountryCode'].str.contains('SP', na=False)

df_filtered = df_filtered[condition1 | condition2]

"""## Missing values"""

# Calculate percentage of missing values per column
missing_percentage = (df_filtered.isnull().sum() / len(df_filtered)) * 100

# Calculate de total number of missing values
total_missing = df_filtered.isnull().sum().sum()
total_percentage_missing = (total_missing / (df.shape[0] * df.shape[1])) * 100

print(f"Overall percentage of missing values: {total_percentage_missing:.2f}%")

# Plotting
missing_percentage.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Percentage of Missing Values Per Column')
plt.ylabel('Percentage (%)')
plt.xlabel('Columns')
plt.show()

# There are some columns with a missing data percentage of near 100% (not only in this new data but also in old ones), that's why we're going to remove them
columns = ['Actor1KnownGroupCode', 'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code',
           'Actor1Type2Code', 'Actor1Type3Code', 'Actor2KnownGroupCode', 'Actor2EthnicCode',
            'Actor2Religion1Code', 'Actor2Religion2Code', 'Actor2Type2Code', 'Actor2Type3Code'
          ]
df_filtered = df_filtered.drop(columns=columns)

# Calculate de total number of missing values for this new filtered data
total_missing = df_filtered.isnull().sum().sum()

total_percentage_missing = (total_missing / (df.shape[0] * df.shape[1])) * 100

print(f"Overall percentage of missing values: {total_percentage_missing:.2f}%")

df_filtered.head()

# Add new filtered samples into the dataset.
mask = ~df_filtered['GLOBALEVENTID'].isin(df_big['GLOBALEVENTID'])
new_entries = df_filtered[mask]

df_big = pd.concat([df_big, new_entries], ignore_index=True)

# Save in trusted zone
df_big.to_csv(os.path.join(TRUSTED_PATH, "articles.csv"), index=False)