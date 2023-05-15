from flask import Flask
from components.data_processor import DataProcessor

app = Flask(__name__)

habitat_path = 'data/raw/habitat.shp'

# Initialize data_processor
data_processor = DataProcessor(habitat_path)


@app.route('/area')
def calculate_area():
    total_area = data_processor.calculate_total_area()
    return str(total_area)


if __name__ == '__main__':
    print("SERVER RUNNING")
    app.run(port=8000, debug=True)
