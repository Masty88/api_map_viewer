from flask import Flask
from components.data_processor import DataProcessor

app = Flask(__name__)

habitat_path = 'data/raw/habitat.shp'

# Initialize data_processor
data_processor = DataProcessor(habitat_path)


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
        return str(specific_area)
    else:
        return f"Group '{group}' not found."


@app.route('/area')
def calculate_total_area():
    total_area = data_processor.calculate_total_area()
    return str(total_area)


@app.route('/percentage/<group>')
def calculate_percentage(group):
    if group in data_processor.groups:
        percentage = data_processor.calculate_area_percentage(data_processor.groups[group])
        formatted_percentage = "{:.1f}".format(percentage)
        return f"{formatted_percentage}%"
    else:
        return f"Group '{group}' not found."


if __name__ == '__main__':
    print("SERVER RUNNING")
    app.run(port=8000, debug=True)
