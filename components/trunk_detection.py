import os

import geojson
import hdbscan
import laspy
import numpy as np
import scipy.spatial
import time
import pandas as pd

# Carica il file LAS
las_file = laspy.read("../data/raw/2546_1200.las")

# Ottieni le coordinate X, Y e Z di tutti i punti
x_coordinates = las_file.x
y_coordinates = las_file.y
z_coordinates = las_file.z

# Ottieni le classificazioni di tutti i punti
classifications = las_file.classification

# Creare la matrice di punti
all_points_xyz = np.column_stack((x_coordinates, y_coordinates, z_coordinates))

# Filtra i punti classificati come suolo
ground_points = all_points_xyz[classifications == 2]

# Ottieni gli indici dei punti del suolo più vicini a ciascun punto
ground_indices = scipy.spatial.cKDTree(ground_points).query(all_points_xyz, k=1, eps=0, p=2)[1]

# Ottieni l'altitudine Z dei punti del suolo più vicini
ground_height = ground_points[ground_indices, 2]

# Filtra i punti classificati come vegetazione che sono tra 0 e 3 metri sopra il suolo
mask = (classifications == 3) & (z_coordinates >= ground_height) & (z_coordinates <= ground_height + 4)

# Filtra le coordinate X, Y e Z con la maschera
x_filtered = x_coordinates[mask]
y_filtered = y_coordinates[mask]
z_filtered = z_coordinates[mask]

# Stampa il numero di punti dopo il filtraggio
print("Numero di punti dopo il filtraggio:", np.sum(mask))

# Select the X, Y, Z coordinates of the filtered points
# Select the X, Y, Z coordinates of the filtered points
filtered_points_xyz = np.column_stack((x_filtered, y_filtered, z_filtered))


# Create an HDBSCAN object and apply the segmentation algorithm
min_cluster_size = 80  # Minimum number of points to form a cluster
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
if os.path.isfile('../data/csv/tree_detection_with_trunk_method.csv'):
    # If the file exists, append without writing the header
    df.to_csv('../data/csv/tree_detection_with_trunk_method.csv', mode='a', header=False, index=False)
else:
    # If the file does not exist, write a new file with a header
    df.to_csv('../data/csv/tree_detection_with_trunk_method.csv', index=False)

features = []  # this will be a list of Feature objects
for label in unique_labels:
    if label != -1:
        clustered_points = filtered_points_xyz[segmented_labels == label]

        # Calculate the height of the highest point in the cluster
        max_height = np.max(clustered_points[:,2])  # assuming that the third column contains the z-coordinates

        # If the max height is at least 4m, process this cluster
        if max_height >= 4:
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
with open("../data/processed/geojson/trunk/cluster_points_geo_3d_trunk_80.geojson", "w") as f:
    geojson.dump(feature_collection, f)

print("Operation completed successfully")


