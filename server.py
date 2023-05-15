from flask import Flask
from components.data_processor import DataProcessor

app = Flask(__name__)

habitat_path = 'data/raw/habitat.shp'

# Initialize data_processor
data_processor = DataProcessor(habitat_path)


@app.route('/area/<group>')
@app.route('/area')
def calculate_area(group=None):
    if group is None:
        total_area = data_processor.calculate_total_area()
        return str(total_area)
    elif group in data_processor.groups:
        specific_area = data_processor.calculate_area(data_processor.groups[group])
        return str(specific_area)
    else:
        return f"Group '{group}' not found."


if __name__ == '__main__':
    print("SERVER RUNNING")
    app.run(port=8000, debug=True)
