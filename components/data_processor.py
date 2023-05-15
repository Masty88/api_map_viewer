import geopandas as gpd
from pathlib import Path

# File path
file_path = "../data/raw/habitat.shp"


class DataProcessor:
    def __init__(self, shapefile_path):
        self.gdf = gpd.read_file(shapefile_path)
        self.gdf['area_km2'] = self.gdf['geometry'].area / 10 ** 6
        self.groups = {
            'forest': ['6', '6.1', '6.2', '6.3', '6.4', '6.5', '6.6'],
        }

    def calculate_total_area(self):
        # Somma dell'area in km^2 per tutti i valori di 'TypoCH'
        total_area = self.gdf['area_km2'].sum()
        print(total_area)
        return total_area

    def calculate_area(self, group):
        # Filter data
        filtered_gdf = self.gdf[self.gdf['TypoCH'].isin(group)]

        # Calculate specify area
        total_area = filtered_gdf['area_km2'].sum()

        return total_area


# data_prc = DataProcessor(file_path).calculate_total_area()
