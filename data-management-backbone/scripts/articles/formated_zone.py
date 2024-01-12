# -*- coding: utf-8 -*-
"""formated_zone.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZZVbqqBTgWP5-sjLzKVqgraDxjL-gvDS
"""

import duckdb
import pandas as pd
import os
from pathlib import Path

# ADSDB_PATH= "C:/Users/inigo/Documents/UPC/ASDB/ASDB/"
PERSISTENT_PATH = "landing/persistent/articles/"
FORMATTED_PATH = "formatted/articles/"
METADATA_PATH = "metadata/"

# Coger ultimo archivo
persistent_paths = [
    Path(PERSISTENT_PATH + file_name)
    for file_name in os.listdir(PERSISTENT_PATH)
]
latest_file = sorted(persistent_paths)[-1]

# 2. Cargar los archivos
header_df = pd.read_excel(os.path.join(METADATA_PATH, "CSV.header.fieldids.xlsx"))
samples_df = pd.read_csv(latest_file, delimiter="\t", header=None)

# Añadir nombre de variables en la tabla
samples_df.columns = header_df.columns

# 3. Mostrar el DataFrame resultante (samples_df)
print(samples_df)

# Save in formatted zone
samples_df.to_csv(os.path.join(FORMATTED_PATH, os.path.basename(latest_file)), index=False)