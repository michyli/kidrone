from flask import Flask, render_template, request, jsonify
import os
import csv

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(
                os.path.abspath(__file__)), '../templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static'))

# Directory where the CSV will be stored
data_directory = os.path.join(os.path.dirname(__file__), '../data')

# Ensure the directory exists
os.makedirs(data_directory, exist_ok=True)

# Path to the CSV file
csv_file_path = os.path.join(data_directory, 'coordinates.csv')
print(f"CSV file path: {csv_file_path}")  # Log the path to check correctness


@app.route('/')
def home():
    return render_template('map.html')


@app.route('/store-coords', methods=['POST'])
def store_coords():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Log received data

        latitude = data['latitude']
        longitude = data['longitude']

        with open(csv_file_path, 'a', newline='') as csvfile:
            fieldnames = ['latitude', 'longitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Move to the end of the file
            csvfile.seek(0, 2)
            if csvfile.tell() == 0:  # Check if file is empty and write header if it is
                writer.writeheader()

            writer.writerow({'latitude': latitude, 'longitude': longitude})
            print(f"Written to CSV: {data}")  # Confirm data has been written

        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error: {str(e)}")  # Log any errors that occur
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
