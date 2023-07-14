from flask import Flask
from components.data_processor import DataProcessor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

habitat_path = 'data/raw/habitat.shp'

# Initialize data_processor
data_processor = DataProcessor(habitat_path)
tree_count = "10706"


@app.route('/area/<group>')
def calculate_specific_area(group):
    """
    Calculate the specific area for a given group.

    Parameters:
    - group (str): The group for which to calculate the area.

    Returns:
    - str: The calculated area.
    """
    if group in data_processor.groups:
        specific_area = data_processor.calculate_specific_area(data_processor.groups[group])
        return "{:.2f}".format(specific_area)
    else:
        return f"Group '{group}' not found."


@app.route('/area')
def calculate_total_area():
    total_area = data_processor.calculate_total_area()
    return "{:.2f}".format(total_area)


@app.route('/percentage/<group>')
def calculate_percentage(group):
    if group in data_processor.groups:
        percentage = data_processor.calculate_area_percentage(data_processor.groups[group])
        formatted_percentage = "{:.1f}".format(percentage)
        return f"{formatted_percentage}%"
    else:
        return f"Group '{group}' not found."


@app.route('/trees')
def get_tree_count():
    """
    Get the calculated tree count from a CSV file.

    Returns:
    - str: The calculated tree count.
    """
    return tree_count


if __name__ == '__main__':
    print("SERVER RUNNING")
    app.run(port=8000, debug=True)
