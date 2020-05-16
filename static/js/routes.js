var markers = L.markerClusterGroup({
  showCoverageOnHover: false,
  zoomToBoundsOnClick: true,
  spiderfyOnMaxZoom: false
});
var polyline = L.polyline({});
var startEndMarkers = L.layerGroup();

$("#map").hide();
$('#loading').hide();
$('#showMap').hide();

$("#showMap").click(function() {
  $("#map").toggle("fast", function() {
    $("#tableDiv").show();
    $('#showMap').hide();
  });
});

jQuery.ajaxSetup({
  beforeSend: function() {
    $('#loading').show();
  },
  complete: function() {
    $('#loading').hide();
  },
  success: function() {}
});

$('#applyFilter').click(function() {
  getRoutes();
})

function getRoutes() {
  if (!$('#route_id').val().trim() && !$('#route_short').val().trim()) {
    alert('Rajaa kyselyä!');
    map.panTo(new L.LatLng(LAT, LON));
    map.setZoom(ZOOM);
    markers.clearLayers();
    map.removeLayer(polyline);

  } else {
    $.ajax({
      url: "/routes",
      type: "POST",
      data: {
        routeID: $('#route_id').val(),
        routeShort: $('#route_short').val()
      },
      timeout: TIMEOUT,
      cache: false,

      success: (res) => {
        $('#tableDiv').show();
        $("#map").hide();
        $("#showMap").hide();
        $('#tableContent').empty();

        response = JSON.parse("[" + res + "]");

        if (response[0].length !== 0) {
          for (i = 0; i < response[0].length; i++) {
            $("#tableContent").append(
              `<tr>
                <td><a onclick="getTrips(${response[0][i].route_id});">${response[0][i].route_id}</a></td>
                <td>${response[0][i].agency_name}</td>
                <td>${response[0][i].route_short_name}</td>
                <td>${response[0][i].route_long_name}</td>
                <td><a href="${response[0][i].agency_url}" target="_blank">${response[0][i].agency_name}</a></td>
              </tr>`
            )
          }
        }
      },

      error: (jqXHR, textStatus) => {
        if (textStatus === "timeout") {
            alert("Pyynnössä kesti liian kauan");
        } else {
            alert("Tietojen hakemisessa tapahtui virhe");
        }
      }
    });
  }
}

function getTrips(route_id) {
  $.ajax({
    url: "/trips",
    type: "POST",
    data: { routeID: route_id },
    timeout: TIMEOUT,
    cache: false,

    success: (res) => {
      $('#tripModal').modal('show');
      $('#tripTable').empty();

      response = JSON.parse("[" + res + "]");

      if (response[0].length !== 0) {
        for (i = 0; i < response[0].length; i++) {
          $("#tripTable").append(
            `<tr>
              <td>${response[0][i].trip_id}</td>
              <td>${response[0][i].trip_headsign}</td>
              <td>${response[0][i].service_id}</td>
              <td><a onclick="getStops('${response[0][i].trip_id}', '${response[0][i].trip_headsign}');">Pysäkit</a></td>
              <td><a onclick="getDates('${response[0][i].trip_id}');">Päivämäärät</a></td>
            </tr>`
          )
        }
      }
    },

    error: (jqXHR, textStatus) => {
      if (textStatus === "timeout") {
          alert("Pyynnössä kesti liian kauan");
      } else {
          alert("Tietojen hakemisessa tapahtui virhe");
      }
    }
  });
}

function getStops(trip_id, trip_headsign) {
  $('#tripModal').modal('hide');

  markers.clearLayers();
  startEndMarkers.clearLayers();
  map.removeLayer(polyline);

  $.ajax({
    url: "/tripStops",
    type: "POST",
    data: { tripID: trip_id },
    timeout: TIMEOUT,
    cache: false,

    success: (res) => {
      $('#tableDiv').hide();

      response = JSON.parse("[" + res + "]");
      var latlngs = Array();

      if (response[0].length !== 0) {
        for (i = 0; i < response[0].length; i++) {
          var newIcon = null;

          if (i === 0) {
            newIcon = new L.Icon({
              iconUrl: '../static/img/marker-icon-green.png',
              iconSize: [25, 41],
              iconAnchor: [12, 41],
              popupAnchor: [1, -34],
              shadowSize: [41, 41]
            });
          } else if (i === response[0].length - 1) {
            newIcon = new L.Icon({
              iconUrl: '../static/img/marker-icon-red.png',
              iconSize: [25, 41],
              iconAnchor: [12, 41],
              popupAnchor: [1, -34],
              shadowSize: [41, 41]
            });
          } else {
            newIcon = new L.Icon({
              iconUrl: '../static/img/marker-icon-blue.png',
              iconSize: [25, 41],
              iconAnchor: [12, 41],
              popupAnchor: [1, -34],
              shadowSize: [41, 41]
            });
          }

          var marker = L.marker([response[0][i].stop_lat, response[0][i].stop_lon], { icon: newIcon });

          marker.bindPopup(
            `<b>Matkan tunniste: </b>${trip_id}<br />
            <b>Määränpää: </b>${trip_headsign}<br /><br />

            <b>Pysäkkiketju: </b>${response[0][i].stop_sequence}<br />
            <b>Saapumisaika: </b>${response[0][i].arrival_time}<br />
            <b>Lähtöaika: </b>${response[0][i].departure_time}<br/><br />

            <b>Pysäkin tunniste: </b>${response[0][i].stop_id}<br />
            <b>Pysäkin nimi: </b>${response[0][i].stop_name}<br />
            <b>Lat-koordinaatti: </b>${response[0][i].stop_lat}<br />
            <b>Lng-koordinaatti: </b>${response[0][i].stop_lon}<br />`
          );
          latlngs.push(marker.getLatLng());

          if (i === 0 || i === response[0].length - 1) {
            marker.addTo(startEndMarkers);
          } else {
            markers.addLayer(marker);
          }

        }

        polyline = L.polyline(latlngs, { color: '#337ab7', smoothFactor: 0.1 }).addTo(map);
        map.fitBounds(polyline.getBounds());

        map.addLayer(markers);
        map.addLayer(startEndMarkers);

        $("#map").show();
        $("#showMap").show();
      }
    },

    error: (jqXHR, textStatus) => {
      if (textStatus === "timeout") {
          alert("Pyynnössä kesti liian kauan");
      } else {
          alert("Tietojen hakemisessa tapahtui virhe");
      }
    }
  });
}
