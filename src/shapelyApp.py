# src/shapelyApp.py
from flask import Flask, request, jsonify, render_template
from .basic_functions import shp2coords
import os

app = Flask(__name__, template_folder='../templates',
            static_folder='../static')

UPLOAD_FOLDER = '../uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('map.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'shapelyFile' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['shapelyFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Check for required shapefile components
        base_name = os.path.splitext(file_path)[0]
        required_extensions = ['.shp', '.shx', '.dbf']
        missing_files = [
            ext for ext in required_extensions if not os.path.exists(base_name + ext)]

        if missing_files:
            return jsonify({'error': f'Missing shapefile components: {", ".join(missing_files)}'})

        try:
            coords = shp2coords(file_path)
            return jsonify({'coords': coords})
        except Exception as e:
            return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Changed port to 5001
