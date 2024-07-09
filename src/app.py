import matplotlib
from flask import Flask, request, jsonify, render_template, send_from_directory, session
import matplotlib.pyplot as plt
import os
from optimization import *
import io
import pandas as pd

app = Flask(__name__, template_folder='../templates',
            static_folder='../static')
app.secret_key = 'supersecretkey'  # Required for session management

# Use Agg backend for Matplotlib
matplotlib.use('Agg')

STATIC_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../static')


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
        debug_info.append(
            f"Using previously uploaded file: {session['filename']}"
        )
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
    file_path = os.path.join(STATIC_DIR, session['filename'])
    with open(file_path, 'wb') as f:
        f.write(session['file'])

    # Extract coords from the uploaded CSV file
    points = csv2coords(file_path)
    debug_info.append(f"Extracted coordinates from CSV: {points}")

    # Construct the best path and measure runtime
    best_path, runtime = construct_best_path(points, disp_diam)
    debug_info.append(f"Constructed best path: {best_path}")
    debug_info.append(
        f"Runtime for constructing the best path: {runtime:.2f} seconds")

    # Save the plot to a file in the static directory
    plot_filename = 'best_path.png'
    plot_path = os.path.join(STATIC_DIR, plot_filename)
    plt.figure(figsize=(16, 8))
    showpath(best_path)
    plt.savefig(plot_path)
    plt.close()
    debug_info.append(f"Saved plot to {plot_path}")

    return jsonify({'result': 'Optimized path calculated. Check the plot.', 'plot_path': plot_filename, 'runtime': runtime, 'debug': debug_info})


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True)
