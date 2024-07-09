var map, view, graphicsLayer;

require([
    "esri/Map",
    "esri/views/MapView",
    "esri/Graphic",
    "esri/layers/GraphicsLayer",
], function (Map, MapView, Graphic, GraphicsLayer) {
    map = new Map({
        basemap: "streets",
    });
    view = new MapView({
        container: "viewDiv",
        map: map,
        center: [-79.4637, 43.6465],
        zoom: 15,
    });
    graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);
    view.on("click", function (event) {
        var lat = event.mapPoint.latitude;
        var lon = event.mapPoint.longitude;
        var point = {
            type: "point",
            longitude: lon,
            latitude: lat,
        };
        var simpleMarkerSymbol = {
            type: "simple-marker",
            color: [226, 119, 40],
            outline: {
                color: [255, 255, 255],
                width: 1,
            },
        };
        var pointGraphic = new Graphic({
            geometry: point,
            symbol: simpleMarkerSymbol,
        });
        graphicsLayer.add(pointGraphic);
        fetch("/store-coords", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ latitude: lat, longitude: lon }),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("Success:", data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    });
});

function submitForm() {
    const form = document.getElementById("optimize-form");
    const formData = new FormData(form);
    fetch("/optimize", {
        method: "POST",
        body: formData,
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
            plot.src = `/static/${data.plot_path}`;
            plotDiv.appendChild(plot);
            drawPathOnMap(data.best_path);
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
                    [segment.start.longitude, segment.start.latitude],
                    [segment.end.longitude, segment.end.latitude],
                ],
            };
            console.log("Polyline details:", polyline);
            const simpleLineSymbol = {
                type: "simple-line",
                color: "#8A2BE2",
                width: "2",
            };
            const polylineGraphic = new Graphic({
                geometry: polyline,
                symbol: simpleLineSymbol,
            });
            graphicsLayer.add(polylineGraphic);
        });
    });
}
