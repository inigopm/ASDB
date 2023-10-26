# -*- coding: utf-8 -*-
"""landing_zone.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17-f_ppP7zvEUMSlol96nivNwBdsWujj5

# Landing zone
"""

import pandas as pd
import shutil
import datetime

LANDING_PATH = "landing/"
TEMPORAL_PATH = "temporal/"
PERSISTENT_PATH = "persistent/"


"""
Modify these fields according to the file you want to ingest
"""
LANDING_ZONE_FILE = "laciudadaldia.csv"

PERSISTENT_DIR = "laciudadaldia/"
PERSISTENT_FILE_NAME = "laciudadaldia"
PERSISTENT_FILE_EXT = ".csv"

source_path = LANDING_PATH + TEMPORAL_PATH + LANDING_ZONE_FILE

ingestion_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
destination_path = (LANDING_PATH
                    + PERSISTENT_PATH
                    + PERSISTENT_DIR
                    + PERSISTENT_FILE_NAME
                    + ingestion_time
                    + PERSISTENT_FILE_EXT)

print(f"Copying temporary file '{source_path}' to persistent file '{destination_path}'...")
shutil.copy(source_path, destination_path)