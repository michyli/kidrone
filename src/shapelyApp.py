from flask import Flask, request, render_template, jsonify, send_from_directory
import geopandas as gpd
import json
import os
import tempfile

app = Flask(__name__, template_folder='../templates')

DEFAULT_POLYGONS = [
    [
        [-8847676.939139081, 5411363.349849086],
        [-8847098.426908756, 5411434.673658196],
        [-8846565.149872905, 5410819.155903677],
        [-8846419.759031257, 5409852.645510843],
        [-8847289.668770544, 5409696.897601154],
        [-8847833.666771423, 5410383.8231410105]
    ],
    [
        [-8846537.71763863, 5412307.354612987],
        [-8845743.94634549, 5412557.799715069],
        [-8845000.812717449, 5412302.735920481],
        [-8845141.220969604, 5411477.305589623],
        [-8846032.796575554, 5411680.947940986]
    ],
    [
        [-8845134.61483972, 5410720.42785237],
        [-8844280.856528161, 5411424.1486377],
        [-8843871.780332584, 5410885.944996509],
        [-8844573.317736002, 5410109.920679417]
    ]
]


def generate_polygons(data):
    # TODO: do your shp2coords magic here
    return json.dumps(data)


@app.route('/')
def index():
    return render_template('shapeMap.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify(success=False, error="No files part")

    files = request.files.getlist('files')
    if not files or len(files) < 3:
        return jsonify(success=False, error="At least three shapefile components (.shp, .shx, .dbf) are required")

    temp_dir = tempfile.mkdtemp()

    for file in files:
        file.save(os.path.join(temp_dir, file.filename))

    shp_path = [os.path.join(temp_dir, f.filename) for f in files if f.filename.endswith('.shp')][0]

    try:
        gdf = gpd.read_file(shp_path)
        data = json.loads(gdf.to_json())
    except Exception as e:
        return jsonify(success=False, error=str(e))

    polygons = generate_polygons(data)
    with open(os.path.join(os.path.dirname(__file__), '..', 'polygons.json'), 'w') as f:
        f.write(polygons)

    return jsonify(success=True)


@app.route('/polygons.json')
def get_polygons():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..'), 'polygons.json')


if __name__ == '__main__':
    app.run(debug=True)
