import os

import geopandas as gpd

# # Carica i dati
# gdf = gpd.read_file('habitat.shp')
# # Calcola l'area in km^2
# gdf['area_km2'] = gdf['geometry'].area / 10**6
#
# print(gdf['TypoCH'].unique())
#
# # Filtra i dati per i valori di interesse in 'TypoCH'
# typoCH_values = ['5', '5.1', '5.2', '5.3']
# filtered_gdf = gdf[gdf['TypoCH'].isin(typoCH_values)]
# print(filtered_gdf)
#
# # Calcola l'area totale per ciascun valore di 'TypoCH'
# total_area_by_TypoCH = filtered_gdf.groupby('TypoCH')['area_km2'].sum()
#
# # Stampa i risultati
# print(total_area_by_TypoCH)


# Carica i dati
gdf = gpd.read_file('data/raw/habitat.shp')
# Calcola l'area in km^2
gdf['area_km2'] = gdf['geometry'].area / 10**6

# Somma dell'area in km^2 per tutti i valori di 'TypoCH'
total_area = gdf['area_km2'].sum()

# Stampa il risultato
print(total_area)