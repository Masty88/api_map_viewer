import geopandas as gpd
from pathlib import Path

# File path
file_path = "../data/raw/habitat.shp"


class DataProcessor:
    def __init__(self, shapefile_path):
        self.gdf = gpd.read_file(shapefile_path)
        self.gdf['area_km2'] = self.gdf['geometry'].area / 10 ** 6

        categories = self.gdf['TypoCH'].unique()
        categories_starting_with_6 = [cat for cat in categories if cat.startswith('6')]
        categories_starting_with_6.sort()
        categories_str = ', '.join(categories_starting_with_6)
        self.groups = {
            'forest': ['6', '6.0', '6.2', '6.2.1', '6.2.3', '6.2.4', '6.2.5', '6.3.2', '6.3.3', '6.3.8', '6.4.1',
                       '6.4.2', '6.4.3', '6.6.1', '6.6.2'],
        }

    def calculate_total_area(self):
        # Somma dell'area in km^2 per tutti i valori di 'TypoCH'
        total_area = self.gdf['area_km2'].sum()

        print(self.groups)
        return total_area

    def calculate_specific_area(self, group):
        # Filter data
        filtered_gdf = self.gdf[self.gdf['TypoCH'].isin(group)]

        # Calculate specify area
        total_area = filtered_gdf['area_km2'].sum()

        return total_area

    def calculate_area_percentage(self, group):
        total_area = self.calculate_total_area()
        forest_area = self.calculate_specific_area(group)
        print("forest", forest_area)
        print("total", total_area)
        forest_percentage = (forest_area / total_area) * 100
        formatted_percentage = "{:.1f}".format(forest_percentage)
        print(formatted_percentage)
        print("forest pouircentage is", formatted_percentage, "%")
        return forest_percentage


# data_prc_forest = DataProcessor(file_path).groups['forest']
# print(data_prc_forest)
# data_prc = DataProcessor(file_path).calculate_area_percentage(data_prc_forest)
