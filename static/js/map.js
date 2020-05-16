var LAT = 65.304401;
var LON = 24.301758;
var ZOOM = 5;
var TIMEOUT = 30000;

var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('http://api.digitransit.fi/map/v1/{id}/{z}/{x}/{y}.png', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ',
  id: 'hsl-map'
}).addTo(map);

map.setView(new L.LatLng(LAT, LON), ZOOM);
