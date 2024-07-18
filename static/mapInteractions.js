var map, view, graphicsLayer;

require([
    "esri/Map",
    "esri/views/MapView",
    "esri/Graphic",
    "esri/layers/GraphicsLayer",
    "esri/geometry/Polygon",
    "esri/geometry/Point"
], function (Map, MapView, Graphic, GraphicsLayer, Polygon, Point) {
    var map = new Map({
        basemap: "streets"
    });

    var view = new MapView({
        container: "viewDiv",
        map: map,
        center: [-79.4637, 43.6465],
        zoom: 15,
        spatialReference: { wkid: 3857 },
    });

    var graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);

    function addPolygonsAndPoints(polygons) {
        var combinedExtent = null;

        polygons.forEach(function (polygonCoordinates) {
            var polygon = new Polygon({
                rings: polygonCoordinates,
                spatialReference: { wkid: 3857 },
            });

            var polygonGraphic = new Graphic({
                geometry: polygon,
                symbol: {
                    type: "simple-fill",
                    color: [227, 139, 79, 0.8],
                    outline: {
                        color: [255, 255, 255],
                        width: 1,
                    },
                },
            });

            graphicsLayer.add(polygonGraphic);

            polygonCoordinates.forEach(function (pointCoords) {
                var point = new Point({
                    x: pointCoords[0],
                    y: pointCoords[1],
                    spatialReference: { wkid: 3857 },
                });

                var pointGraphic = new Graphic({
                    geometry: point,
                    symbol: {
                        type: "simple-marker",
                        color: "blue",
                        size: "8px",
                    },
                });

                graphicsLayer.add(pointGraphic);

                if (combinedExtent) {
                    combinedExtent = combinedExtent.union(polygonGraphic.geometry.extent);
                } else {
                    combinedExtent = polygonGraphic.geometry.extent.clone();
                }
            });
        });

        if (combinedExtent) {
            view.goTo(combinedExtent);
        }
    }

    document.getElementById("upload-form").addEventListener("submit", function(event) {
        event.preventDefault();
        var form = event.target;
        var formData = new FormData(form);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            var resultDiv = document.getElementById("result");
            if (result.success) {
                fetch("/data/polygons.json")
                .then(response => response.json())
                .then(polygons => {
                    console.log("Polygons loaded:", polygons);
                    addPolygonsAndPoints(polygons);
                })
                .catch(error => {
                    console.error("Error loading polygons:", error);
                });
            } else {
                resultDiv.textContent = "File upload failed: " + result.error;
                resultDiv.style.display = "block";
            }
        })
        .catch(error => {
            console.error("Error uploading file:", error);
        });
    });

    window.submitForm = function() {
        const form = document.getElementById("optimize-form");
        const formData = new FormData(form);
        fetch("/optimize", {
            method: "POST",
            body: formData
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.error) {
                document.getElementById("output").innerText = data.error;
            } else {
                document.getElementById("output").innerText = data.result;
                const plotDiv = document.getElementById("plot");
                plotDiv.innerHTML = "";
                const plot = document.createElement("img");
                plot.src = `${data.plot_path}`;
                plotDiv.appendChild(plot);
                if (data.best_path_coords) {
                    drawPathOnMap(data.best_path_coords);
                } else {
                    console.error("No best path coordinates returned.");
                }
            }
            const debugDiv = document.getElementById("debug");
            debugDiv.innerHTML = "";
            data.debug.forEach((line) => {
                const p = document.createElement("p");
                p.innerText = line;
                debugDiv.appendChild(p);
            });
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }
    
    

    function drawPathOnMap(pathDetails) {
        console.log("Drawing path with details:", pathDetails);
        require(["esri/Graphic"], function (Graphic) {
            pathDetails.forEach((segment) => {
                const polyline = {
                    type: "polyline",
                    paths: [
                        [segment.start.x, segment.start.y],
                        [segment.end.x, segment.end.y]
                    ],
                    spatialReference: { wkid: 3857 }
                };

                const simpleLineSymbol = {
                    type: "simple-line",
                    color: "#8A2BE2",
                    width: "2"
                };

                const polylineGraphic = new Graphic({
                    geometry: polyline,
                    symbol: simpleLineSymbol
                });
                graphicsLayer.add(polylineGraphic);
            });
        });
    }
});
