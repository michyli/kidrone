require([
    "esri/config",
     "esri/Map",
     "esri/views/MapView"
   ],(esriConfig, Map, MapView)=> {

     esriConfig.apiKey= "YOUR_ACCESS_TOKEN";
     const map = new Map({
       basemap: "arcgis/topographic" // Basemap layer
     });

     const view = new MapView({
       map: map,
       center: [-118.805, 34.027],
       zoom: 13, // scale: 72223.819286
       container: "viewDiv",
       constraints: {
         snapToZoom: false
       }
     });

   });