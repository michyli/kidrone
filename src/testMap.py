# from flask import Flask, render_template
# import arcgis
# from arcgis.gis import GIS
# import os

# print("Current working directory:", os.getcwd())

# app = Flask(__name__, template_folder=os.path.join(
#     os.path.dirname(__file__), '../templates'))


# @app.route('/')
# def home():
#     gis = GIS()
#     map1 = gis.map('Paris')
#     return render_template('map.html', map_widget=map1)


# if __name__ == '__main__':
#     app.run(debug=True)
