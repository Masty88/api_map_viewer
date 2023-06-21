# import hdbscan as hdbscan
# import laspy
# import numpy as np
# import geojson
#
# # Carica il file LAS
# las_file = laspy.read("../data/raw/points_lidar_2016_vegetation.las")
#
# # Ottieni le coordinate X, Y e Z di tutti i punti
# x_coordinates = las_file.x
# y_coordinates = las_file.y
# z_coordinates = las_file.z
# print("Altitudine minima:", np.min(z_coordinates))
#
# # Filtra i punti che hanno un'altitudine superiore a 3 metri
# mask = z_coordinates > 583
# x_coordinates = x_coordinates[mask]
# y_coordinates = y_coordinates[mask]
# z_coordinates = z_coordinates[mask]
#
# print("Numero di punti dopo il filtraggio:", len(x_coordinates))
#
# # Seleziona le coordinate X, Y, Z dei punti filtrati
# all_points_xyz = np.column_stack((x_coordinates, y_coordinates, z_coordinates))
#
# # Crea un oggetto HDBSCAN e applica l'algoritmo di segmentazione
# min_cluster_size = 120  # Numero minimo di punti per formare un cluster
# print("Calcolo dei cluster in corso...")
# clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)
# segmented_labels = clusterer.fit_predict(all_points_xyz)
#
# # Verifica se HDBSCAN ha calcolato i cluster correttamente
# if hasattr(clusterer, 'labels_'):
#     print("HDBSCAN ha calcolato i cluster.")
# else:
#     print("HDBSCAN non ha calcolato i cluster correttamente.")
#
# unique_labels = np.unique(segmented_labels)
#
# num_clusters = len(unique_labels) - 1  # Sottrai 1 per escludere il cluster di rumore (etichetta -1)
# print("Numero di cluster:", num_clusters)
#
# features = []  # questa sarà una lista di oggetti Feature
# for label in unique_labels:
#     if label != -1:
#         clustered_points = all_points_xyz[segmented_labels == label]
#
#         # Calcola il centroide del cluster
#         centroid = np.mean(clustered_points, axis=0)
#
#         # Crea una geometria Point per il centroide
#         centroid_geojson = geojson.Point((centroid[0], centroid[1], centroid[2]))
#
#         # Crea un oggetto Feature per il centroide
#         feature = geojson.Feature(geometry=centroid_geojson)
#
#         # Aggiungi l'oggetto Feature alla lista
#         features.append(feature)
#
# # Crea una feature collection GeoJSON
# feature_collection = geojson.FeatureCollection(features)
#
# # Salva la feature collection GeoJSON su disco
# with open("cluster_points_geo_3d_120.geojson", "w") as f:
#     geojson.dump(feature_collection, f)
import os

import hdbscan as hdbscan
import laspy
import numpy as np
import geojson
import scipy.spatial
import pandas as pd
import time

# Load the LAS file
las_file = laspy.read("../data/raw/2554_1200.las")

# Get the X, Y, and Z coordinates of all points
x_coordinates = las_file.x
y_coordinates = las_file.y
z_coordinates = las_file.z

# Get the classifications of all points
classifications = las_file.classification

# Create the point matrix
all_points_xyz = np.column_stack((x_coordinates, y_coordinates, z_coordinates))

# Filter points classified as ground
ground_points = all_points_xyz[classifications == 2]

# Calculate minimum altitude of each ground point
ground_height = scipy.spatial.cKDTree(ground_points).query(all_points_xyz, k=1, eps=0, p=2)[0]

# Filter points classified as vegetation that are 4 meters or more above the ground point
# mask = (classifications == 3) & (z_coordinates - ground_height >= 4)


x_coordinates = x_coordinates[mask]
y_coordinates = y_coordinates[mask]
z_coordinates = z_coordinates[mask]

print("Number of points after filter:", len(x_coordinates))

# Select the X, Y, Z coordinates of the filtered points
filtered_points_xyz = np.column_stack((x_coordinates, y_coordinates, z_coordinates))

# Create an HDBSCAN object and apply the segmentation algorithm
min_cluster_size = 10  # Minimum number of points to form a cluster
print("Calculating clusters...")
start_time = time.time()
clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)
segmented_labels = clusterer.fit_predict(filtered_points_xyz)


# Check if HDBSCAN calculated the clusters correctly
if hasattr(clusterer, 'labels_'):
    print("HDBSCAN has calculated the clusters.")
else:
    print("HDBSCAN has not calculated the clusters correctly.")

unique_labels = np.unique(segmented_labels)

num_clusters = len(unique_labels) - 1  # Subtract 1 to exclude the noise cluster (label -1)
print("Number of clusters:", num_clusters)

end_time = time.time()
# Calculate the elapsed time
time_elapsed = (end_time - start_time) / 60

# Create a DataFrame
df = pd.DataFrame({
    'Date': [pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')],
    'File Name': ["../data/raw/2554_1200.las"],
    'Min Cluster Size': [min_cluster_size],
    'Unique Labels': [num_clusters],
    'Time Elapsed': [time_elapsed]
})

# Check if the file exists
if os.path.isfile('../data/csv/tree_detection_with_crown_method.csv'):
    # If the file exists, append without writing the header
    df.to_csv('../data/csv/tree_detection_with_crown_method.csv', mode='a', header=False, index=False)
else:
    # If the file does not exist, write a new file with a header
    df.to_csv('../data/csv/tree_detection_with_crown_method.csv', index=False)

features = []  # this will be a list of Feature objects
for label in unique_labels:
    if label != -1:
        clustered_points = filtered_points_xyz[segmented_labels == label]

        # Calculate the centroid of the cluster
        centroid = np.mean(clustered_points, axis=0)

        # Create a Point geometry for the centroid
        centroid_geojson = geojson.Point((centroid[0], centroid[1], centroid[2]))

        # Create a Feature object for the centroid
        feature = geojson.Feature(geometry=centroid_geojson)

        # Add the Feature object to the list
        features.append(feature)

# Create a GeoJSON feature collection
feature_collection = geojson.FeatureCollection(features)

# Save the GeoJSON feature collection to disk
with open("../data/processed/geojson/trunk/cluster_points_geo_3d_10_3m.geojson", "w") as f:
    geojson.dump(feature_collection, f)

print("Operation completed successfully")
