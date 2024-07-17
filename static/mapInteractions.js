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
        center: [ -115.749, 49.396],
        zoom: 15,
        spatialReference: { wkid: 3857 },
    });

    var graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);

    // view.on("click", function (event) {
    //     var point = new Point({
    //         x: event.mapPoint.x,
    //         y: event.mapPoint.y,
    //         spatialReference: { wkid: 3857 }
    //     });

    //     var simpleMarkerSymbol = {
    //         type: "simple-marker",
    //         color: [226, 119, 40],
    //         outline: {
    //             color: [255, 255, 255],
    //             width: 1
    //         }
    //     };

    //     var pointGraphic = new Graphic({
    //         geometry: point,
    //         symbol: simpleMarkerSymbol
    //     });
    //     graphicsLayer.add(pointGraphic);

    //     fetch("/store-coords", {
    //         method: "POST",
    //         headers: {
    //             "Content-Type": "application/json"
    //         },
    //         body: JSON.stringify({ x: event.mapPoint.x, y: event.mapPoint.y })
    //     })
    //     .then((response) => response.json())
    //     .then((data) => {
    //         console.log("Success:", data);
    //     })
    //     .catch((error) => {
    //         console.error("Error:", error);
    //     });
    // });
    function addPolygonsAndPoints(polygons) {
    var combinedExtent = null;

    polygons.forEach(function (polygonCoordinates) {
      // Create a polygon geometry
      var polygon = new Polygon({
        rings: polygonCoordinates,
        spatialReference: { wkid: 3857 },
      });

      // Create a polygon graphic
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

      // Add the polygon graphic to the graphics layer
      graphicsLayer.add(polygonGraphic);

      // Add points to the map
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

        // Update the combined extent
        if (combinedExtent) {
          combinedExtent = combinedExtent.union(polygonGraphic.geometry.extent);
        } else {
          combinedExtent = polygonGraphic.geometry.extent.clone();
        }  
      });
    });
    // Zoom to the combined extent of all polygons
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
          fetch("/polygons.json")
            .then((response) => response.json())
            .then((polygons) => {
              console.log("Polygons loaded:", polygons); // Log the loaded polygons
              addPolygonsAndPoints(polygons);
            })
            .catch((error) => {
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

    function submitForm() {
    const form = document.getElementById("optimize-form");
    const formData = new FormData(form);
    fetch("/optimize", {
        method: "POST",
        body: formData
    })
    .then((response) => response.json())
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
