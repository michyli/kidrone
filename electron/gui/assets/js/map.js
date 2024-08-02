require([
  "esri/config",
  "esri/Map",
  "esri/views/MapView",
  "esri/Graphic",
  "esri/layers/GraphicsLayer",
  "esri/geometry/Polygon",
  "esri/geometry/Point"
], function (esriConfig, Map, MapView, Graphic, GraphicsLayer, Polygon, Point) {
  // Set your ArcGIS API key (uncomment and set if needed)
  // esriConfig.apiKey = "YOUR_ACCESS_TOKEN";
  
  // Create a map with a topographic basemap
  const map = new Map({
      basemap: "streets" // Basemap layer
  });

  // Create a MapView to display the map
  const view = new MapView({
      container: "viewDiv", // Reference to the map container in the HTML
      map: map,
      center: [-118.805, 34.027], // Longitude, latitude
      zoom: 13 // Zoom level
  });

  const graphicsLayer = new GraphicsLayer();
  map.add(graphicsLayer);

  function addPolygonsAndPoints(polygons) {
      let combinedExtent = null;

      polygons.forEach(function (polygonCoordinates) {
          const polygon = new Polygon({
              rings: [polygonCoordinates],
              spatialReference: { wkid: 3857 },
          });

          const polygonGraphic = new Graphic({
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
              const point = new Point({
                  x: pointCoords[0],
                  y: pointCoords[1],
                  spatialReference: { wkid: 3857 },
              });

              const pointGraphic = new Graphic({
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

  document.getElementById("saveBlockBtn").addEventListener("click", function() {
      const fileInput = document.getElementById("uploadShape");
      const files = fileInput.files;

      if (files.length === 0) {
          alert("Please upload a shapefile.");
          return;
      }

      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
          formData.append("files[]", files[i]);
      }

      fetch("http://localhost:8000/upload", {
          method: "POST",
          body: formData
      })
      .then(response => response.json())
      .then(result => {
          if (result.success) {
              fetch("http://localhost:8000/uploads/polygons.json")
              .then(response => response.json())
              .then(polygons => {
                  console.log("Polygons loaded:", polygons);
                  addPolygonsAndPoints(polygons);
              })
              .catch(error => {
                  console.error("Error loading polygons:", error);
              });
          } else {
              document.getElementById("result").textContent = "File upload failed: " + result.error;
              document.getElementById("result").style.display = "block";
          }
      })
      .catch(error => {
          console.error("Error uploading file:", error);
      });
  });
});
