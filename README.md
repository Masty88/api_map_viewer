# API Documentation

## Introduction
This API provides endpoints to calculate areas and percentages based on groups. The API was created to work with the <map-viewer> web components. This document will be updated with information on how to use the clustering function to identify and group similar data points, for example to identify different land use types or vegetation groups in an urban twin map. This could be useful for example for city planning, ecological studies or even virtual reality applications.
## Installation
1. Clone the repository: `git clone https://github.com/your/repository.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the server: `python app.py`

## Endpoints

### Calculate Specific Area
Calculates the specific area for a given group.

- **URL**: `/area/<group>`
- **Method**: GET
- **Parameters**:
  - `group` (string): The group for which to calculate the area.
- **Response**:
  - Success: The calculated area.
  - Error: "Group '{group}' not found."

### Calculate Total Area
Calculates the total area.

- **URL**: `/area`
- **Method**: GET
- **Response**:
  - The calculated total area.

### Calculate Percentage
Calculates the percentage of the total area for a given group.

- **URL**: `/percentage/<group>`
- **Method**: GET
- **Parameters**:
  - `group` (string): The group for which to calculate the percentage.
- **Response**:
  - Success: The calculated percentage.
  - Error: "Group '{group}' not found."

## Examples

### Calculate Specific Area
Request:
GET /area/forest

makefile
Copy code
Response:
256.78

makefile
Copy code

### Calculate Total Area
Request:
GET /area

makefile
Copy code
Response:
1024.56

makefile
Copy code

### Calculate Percentage
Request:
GET /percentage/forest

makefile
Copy code
Response:
25.0%

csharp
Copy code

### Clustering Function
This function is used to identify and group similar data points. It is a method based on HDBSCAN algorithm which is a density-based clustering method particularly suited to spatial data. This function is not accessible via the API but the code can be used directly for those who need it.

The clustering function uses the HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise) algorithm to identify and group similar data points. This function is particularly well suited to spatial data and can identify clusters of any shape, unlike other clustering algorithms such as K-means.

The clustering function can be found in the repository. For more information on how to use the clustering function, refer to the HDBSCAN documentation.
## License
This project is licensed under the [MIT License](https://opensource.org/lic