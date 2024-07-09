from flask import Flask, render_template, request, jsonify
import os
import csv

app = Flask(__name__, template_folder=os.path.join(
    os.path.dirname(__file__), '../templates'))

# Directory where the CSV will be stored
data_directory = os.path.join(os.path.dirname(__file__), '../data')

# Ensure the directory exists
os.makedirs(data_directory, exist_ok=True)

# Path to the CSV file
csv_file_path = os.path.join(data_directory, 'coordinates.csv')


@app.route('/')
def home():
    return render_template('map.html')


@app.route('/store-coords', methods=['POST'])
def store_coords():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']

    with open(csv_file_path, 'a', newline='') as csvfile:
        fieldnames = ['latitude', 'longitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the file is empty to write header
        csvfile.seek(0, 2)  # Move to the end of the file
        if csvfile.tell() == 0:  # Check if file is empty
            writer.writeheader()  # Write header if empty

        writer.writerow({'latitude': latitude, 'longitude': longitude})

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
