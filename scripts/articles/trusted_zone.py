ADSDB_PATH= "C:/Users/inigo/Documents/UPC/ASDB/ASDB/"
FORMATTED_PATH = "formatted/articles/"
TRUSTED_PATH = "trusted/articles/"
METADATA_PATH = "metadata/"

import duckdb
import pandas as pd
import os
from pathlib import Path

# Coger ultimo archivo
formatted_paths = [
    Path(ADSDB_PATH + FORMATTED_PATH + file_name)
    for file_name in os.listdir(ADSDB_PATH + FORMATTED_PATH)
]
latest_file = sorted(formatted_paths)[-1]

# Cargar archivo
df = pd.read_csv(latest_file)
df_big = pd.read_csv(os.path.join(ADSDB_PATH, TRUSTED_PATH, "articles.csv"))

# Quitar las columnas que no nos interesan
df_filtered = df.iloc[:, 1:].drop(columns=['DATEADDED', 'SOURCEURL', 'MonthYear', 'Year', 'FractionDate'])

# Convertir la columna "SQLDATE" a un objeto datetime
df_filtered['SQLDATE'] = pd.to_datetime(df_filtered['SQLDATE'], format='%Y%m%d')

# Reformatear la fecha al formato deseado y reemplazar la columna original
df_filtered['SQLDATE'] = df_filtered['SQLDATE'].dt.strftime('%Y-%m-%d')

# Filtar por pais y coger solo los articulos relacionados con España.
condition1 = df_filtered['Actor1Geo_CountryCode'].str.contains('SP', na=False)
condition2 = df_filtered['Actor2Geo_CountryCode'].str.contains('SP', na=False)

df_filtered = df_filtered[condition1 | condition2]

print(df_filtered)

# # Conectar con DuckDB
# con = duckdb.connect(database=':memory:', read_only=False)

# # Cargar los archivos en DuckDB y Pandas
# con.execute("CREATE TABLE df AS SELECT * FROM read_csv_auto(?)", (str(latest_file),))
# df_big = pd.read_csv(os.path.join(ADSDB_PATH, TRUSTED_PATH, "articles.csv"))

# # Quitar las columnas que no nos interesan
# columns_to_remove = ['DATEADDED', 'SOURCEURL', 'MonthYear', 'Year', 'FractionDate']
# columns_in_df = con.execute("PRAGMA table_info(df)").fetchdf()['name'].tolist()
# columns_to_select = [col for col in columns_in_df if col not in columns_to_remove]

# # Usar sentencias SQL para operaciones
# sql = f"""
#     SELECT {', '.join(columns_to_select)}
#     FROM df
#     WHERE Actor1Geo_CountryCode LIKE '%%SP%%' OR Actor2Geo_CountryCode LIKE '%%SP%%'
# """

# df_filtered = con.execute(sql).fetchdf()

# con.close()

# # Establecer 'GLOBALEVENTID' como el índice del DataFrame
# df_filtered.set_index('GLOBALEVENTID', inplace=True)
# df_filtered.drop(columns=['column00'], inplace=True)

# # Convertir la columna "SQLDATE" a un objeto datetime
# df_filtered['SQLDATE'] = pd.to_datetime(df_filtered['SQLDATE'], format='%Y%m%d')

# # Reformatear la fecha al formato deseado y reemplazar la columna original
# df_filtered['SQLDATE'] = df_filtered['SQLDATE'].dt.strftime('%Y-%m-%d')

# print(df_filtered)

# Añadir las muestras filtradas al dataset.
# Identificar las filas de df_filtered que no están en df_main
mask = ~df_filtered['GLOBALEVENTID'].isin(df_big['GLOBALEVENTID'])

# Filtrar df_filtered usando la máscara
new_entries = df_filtered[mask]

# Agregar estas nuevas entradas al DataFrame principal
df_big = pd.concat([df_big, new_entries], ignore_index=True)

# Guardarlo en el trusted

df_big.to_csv(os.path.join(ADSDB_PATH, TRUSTED_PATH, "articles.csv"))

print(df_big)