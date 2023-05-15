# API Documentation

## Introduction
This API provides endpoints to calculate areas and percentages based on groups.Api created to work with the <map-viewer> <a href="https://github.com/Masty88/urban-twin">web components </a>

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

## License
This project is licensed under the [MIT License](https://opensource.org/lic