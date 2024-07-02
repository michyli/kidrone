import matplotlib
from flask import Flask, request, jsonify, render_template, send_from_directory, session
import matplotlib.pyplot as plt
import os
from src.optimization import *
import io
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# Use Agg backend for Matplotlib
matplotlib.use('Agg')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/optimize', methods=['POST'])
def optimize():
    debug_info = []
    debug_info.append("Received a request to /optimize")

    # Check if file is uploaded or already stored in session
    if 'csvFile' in request.files:
        file = request.files['csvFile']
        if file.filename == '':
            debug_info.append("No selected file")
            return jsonify({'error': 'No selected file', 'debug': debug_info})

        session['file'] = file.read()
        session['filename'] = file.filename
        debug_info.append(f"File uploaded: {file.filename}")
    elif 'file' in session:
        file = io.BytesIO(session['file'])
        debug_info.append(f"Using previously uploaded file: {
                          session['filename']}")
    else:
        debug_info.append("No file part in the request")
        return jsonify({'error': 'No file part', 'debug': debug_info})

    disp_diam = request.form.get('dispDiam')
    if not disp_diam:
        debug_info.append("Display diameter is required")
        return jsonify({'error': 'Display diameter is required', 'debug': debug_info})

    disp_diam = int(disp_diam)
    debug_info.append(f"Display diameter received: {disp_diam}")

    # Save the uploaded file to the static directory
    file_path = os.path.join('static', session['filename'])
    with open(file_path, 'wb') as f:
        f.write(session['file'])

    # extract coords from the uploaded CSV file
    points = csv2coords(file_path)
    debug_info.append(f"Extracted coordinates from CSV: {points}")

    # construct a list of paths to iterate over
    pathlist = path_list_constructor(points, disp_diam)
    debug_info.append(f"Constructed path list: {pathlist}")

    # calculate the optimized path
    optimized_path = optimizer(pathlist, shortest_airtime())
    debug_info.append(f"Calculated optimized path: {optimized_path}")

    # Save the plot to a file in the static directory
    plot_filename = 'optimized_path.png'
    plot_path = os.path.join('static', plot_filename)
    plt.figure(figsize=(16, 8))
    showpath(optimized_path)
    plt.savefig(plot_path)
    plt.close()
    debug_info.append(f"Saved plot to {plot_path}")

    return jsonify({'result': 'Optimized path calculated. Check the plot.', 'plot_path': plot_filename, 'debug': debug_info})


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(debug=True)
