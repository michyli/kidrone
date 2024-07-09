require([
    "esri/Map",
    "esri/views/MapView",
    "esri/Graphic",
    "esri/layers/GraphicsLayer"
], function (Map, MapView, Graphic, GraphicsLayer) {
    var map = new Map({
        basemap: "streets"  // Choose the basemap suitable for your needs
    });

    var view = new MapView({
        container: "viewDiv",
        map: map,
        center: [-79.4637, 43.6465], // Longitude, Latitude for High Park, Toronto
        zoom: 15  // Increased zoom level for a closer look
    });

    var graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);

    view.on("click", function(event) {
        var lat = event.mapPoint.latitude;
        var lon = event.mapPoint.longitude;

        var point = {
            type: "point",
            longitude: lon,
            latitude: lat
        };

        var simpleMarkerSymbol = {
            type: "simple-marker",
            color: [226, 119, 40], // Orange
            outline: {
                color: [255, 255, 255], // White
                width: 1
            }
        };

        var pointGraphic = new Graphic({
            geometry: point,
            symbol: simpleMarkerSymbol
        });

        graphicsLayer.add(pointGraphic);

        fetch('/store-coords', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ latitude: lat, longitude: lon })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
