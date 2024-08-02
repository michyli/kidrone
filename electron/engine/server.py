import os
import json
import shapefile  # You need to install pyshp (pip install pyshp)
from http.server import BaseHTTPRequestHandler, HTTPServer

UPLOAD_FOLDER = '/Users/qiwen/Downloads/kidrone/electron/gui/assets/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            files = self.parse_multipart(post_data)

            if not all(ext in files for ext in ['shp', 'shx', 'dbf']):
                self.respond(
                    400, {'success': False, 'error': 'Incomplete shapefile'})

            shapefile_path = self.save_shapefile(files)
            polygons = self.process_shapefile(shapefile_path)

            with open(os.path.join(UPLOAD_FOLDER, 'polygons.json'), 'w') as f:
                json.dump(polygons, f)

            self.respond(200, {'success': True})
        else:
            self.respond(404, {'success': False, 'error': 'Not found'})

    def do_GET(self):
        if self.path == '/uploads/polygons.json':
            try:
                with open(os.path.join(UPLOAD_FOLDER, 'polygons.json'), 'r') as f:
                    polygons = json.load(f)
                self.respond(200, polygons)
            except Exception as e:
                self.respond(500, {'success': False, 'error': str(e)})
        else:
            self.respond(404, {'success': False, 'error': 'Not found'})

    def parse_multipart(self, post_data):
        boundary = self.headers['Content-Type'].split('boundary=')[-1]
        parts = post_data.split(boundary.encode())
        files = {}

        for part in parts:
            if b'filename="' in part:
                headers, data = part.split(b'\r\n\r\n', 1)
                headers = headers.decode()
                filename = headers.split('filename="')[1].split('"')[0]
                file_ext = filename.split('.')[-1]
                files[file_ext] = data.rstrip(b'\r\n--')

        return files

    def save_shapefile(self, files):
        base_path = os.path.join(UPLOAD_FOLDER, 'uploaded_shapefile')
        for ext, data in files.items():
            with open(f"{base_path}.{ext}", 'wb') as f:
                f.write(data)
        return f"{base_path}.shp"

    def process_shapefile(self, shapefile_path):
        reader = shapefile.Reader(shapefile_path)
        polygons = []

        for shape in reader.shapes():
            if shape.shapeType == shapefile.POLYGON:
                polygons.append(shape.points)

        return polygons

    def respond(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
