/* // /static/testShapely.js

require([
    "esri/Map",
    "esri/views/MapView",
    "esri/Graphic",
    "esri/layers/GraphicsLayer"
  ], function (Map, MapView, Graphic, GraphicsLayer) {
    var map = new Map({
      basemap: "streets"
    });
  
    var view = new MapView({
      container: "viewDiv",
      map: map,
      zoom: 11,
      spatialReference: {
        wkid: 3857
      }
    });
  
    var graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);
  
    document.getElementById('shapelyFile').addEventListener('change', function(event) {
      var file = event.target.files[0];
      if (file) {
        var formData = new FormData();
        formData.append('shapelyFile', file);
  
        fetch('/upload', {
          method: 'POST',
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            console.error('Error:', data.error);
            alert('Error: ' + data.error);
          } else if (data.coords) {
            // Center the map based on the first coordinate
            if (data.coords.length > 0 && data.coords[0].length > 0) {
              var firstCoord = data.coords[0][0];
              view.center = [firstCoord[0], firstCoord[1]];
            }
            
            // Add points to the map
            data.coords.forEach(function(coordList) {
              coordList.forEach(function(coord) {
                var point = {
                  type: "point",
                  x: coord[0],
                  y: coord[1],
                  spatialReference: {
                    wkid: 3857
                  }
                };
  
                var pointGraphic = new Graphic({
                  geometry: point,
                  symbol: {
                    type: "simple-marker",
                    color: [226, 119, 40], // Orange
                    outline: {
                      color: [255, 255, 255], // White
                      width: 1
                    }
                  }
                });
  
                graphicsLayer.add(pointGraphic);
              });
            });
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('An error occurred while processing the shapefile.');
        });
      }
    });
  });
   */