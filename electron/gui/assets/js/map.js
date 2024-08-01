  require([
      "esri/config",
      "esri/Map",
      "esri/views/MapView"
    ], function(esriConfig, Map, MapView) {
      
      // // Set your ArcGIS API key
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
      
    });