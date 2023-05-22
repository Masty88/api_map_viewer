import hdbscan as hdbscan
import laspy
import numpy as np
import geojson

# Carica il file LAS
las_file = laspy.read("../data/raw/points_lidar_2016_vegetation.las")

# Ottieni le coordinate X, Y e Z di tutti i punti
x_coordinates = las_file.x
y_coordinates = las_file.y
z_coordinates = las_file.z
print("Altitudine minima:", np.min(z_coordinates))

# Filtra i punti che hanno un'altitudine superiore a 3 metri
mask = z_coordinates > 583
x_coordinates = x_coordinates[mask]
y_coordinates = y_coordinates[mask]
z_coordinates = z_coordinates[mask]

print("Numero di punti dopo il filtraggio:", len(x_coordinates))

# Seleziona le coordinate X, Y, Z dei punti filtrati
all_points_xyz = np.column_stack((x_coordinates, y_coordinates, z_coordinates))

# Crea un oggetto HDBSCAN e applica l'algoritmo di segmentazione
min_cluster_size = 120  # Numero minimo di punti per formare un cluster
print("Calcolo dei cluster in corso...")
clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)
segmented_labels = clusterer.fit_predict(all_points_xyz)

# Verifica se HDBSCAN ha calcolato i cluster correttamente
if hasattr(clusterer, 'labels_'):
    print("HDBSCAN ha calcolato i cluster.")
else:
    print("HDBSCAN non ha calcolato i cluster correttamente.")

unique_labels = np.unique(segmented_labels)

num_clusters = len(unique_labels) - 1  # Sottrai 1 per escludere il cluster di rumore (etichetta -1)
print("Numero di cluster:", num_clusters)

features = []  # questa sarà una lista di oggetti Feature
for label in unique_labels:
    if label != -1:
        clustered_points = all_points_xyz[segmented_labels == label]

        # Calcola il centroide del cluster
        centroid = np.mean(clustered_points, axis=0)

        # Crea una geometria Point per il centroide
        centroid_geojson = geojson.Point((centroid[0], centroid[1], centroid[2]))

        # Crea un oggetto Feature per il centroide
        feature = geojson.Feature(geometry=centroid_geojson)

        # Aggiungi l'oggetto Feature alla lista
        features.append(feature)

# Crea una feature collection GeoJSON
feature_collection = geojson.FeatureCollection(features)

# Salva la feature collection GeoJSON su disco
with open("cluster_points_geo_3d_120.geojson", "w") as f:
    geojson.dump(feature_collection, f)
