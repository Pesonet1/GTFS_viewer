var mrks = {}
var markers = L.markerClusterGroup({
  showCoverageOnHover: false,
  zoomToBoundsOnClick: true,
  spiderfyOnMaxZoom: false
});

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
  getStops();
})

function getStops() {
  $('#tableContent').empty();
  markers.clearLayers();

  if (!$('#stop_id').val().trim() && !$('#stop_name').val().trim()) {
    alert('Rajaa kyselyä!');
    map.setView(new L.LatLng(LAT, LON), ZOOM);
  } else {
    $.ajax({
      url: "/stops",
      type: "POST",
      data: {
        stopID: $('#stop_id').val(),
        stopName: $('#stop_name').val()
      },
      timeout: TIMEOUT,
      cache: false,

      success: (res) => {
        $('#tableDiv').show();
        $("#map").hide();
        $("#showMap").hide();
        $('#tableContent').empty();
        
        response = JSON.parse("[" + res + "]")

        if (response[0].length !== 0) {
          marks = {};

          for (i = 0; i < response[0].length; i++) {
            $("#tableContent").append(
              `<tr>
                <td>${response[0][i].stop_id}</td>
                <td>${response[0][i].stop_name}</td>
                <td>${response[0][i].stop_lat}</td>
                <td>${response[0][i].stop_lon}</td>
                <td><a onclick="showStopOnMap('${response[0][i].stop_id}');">Näytä kartalla</a></td>
              </tr>`
            )

            var marker = L.marker([response[0][i].stop_lat, response[0][i].stop_lon]);

            marker.bindPopup(
              `<b>Pysäkin tunnus: </b>${response[0][i].stop_id}<br />
              <b>Pysäkin nimi: </b>${response[0][i].stop_name}<br /><br />
              <b>Lat-koordinaatti: </b>${response[0][i].stop_lat}<br />
              <b>Lon-koordinaatti: </b>${response[0][i].stop_lon}<br /><br />
              <a onclick="getStopRoutes('${response[0][i].stop_id}');">Pysäkin kautta kulkevat reitit</a><br/>`,
              { minWidth: 350, minHeight: 400 }
            );

            markers.addLayer(marker);
            mrks[response[0][i].stop_id] = marker;
          }

          map.addLayer(markers);
          map.fitBounds(markers.getBounds());
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

function showStopOnMap(markerId) {
  $("#map").show();
  $("#showMap").show();
  $("#tableDiv").hide();
  map.closePopup();
  map.setView(new L.LatLng(mrks[markerId]._latlng.lat, mrks[markerId]._latlng.lng), 18);
  setTimeout(() => {
    mrks[markerId].openPopup();
  }, 500);
}

function getStopRoutes(stop_id) {
  $('#routeTableContent').empty();

  $.ajax({
    url: "/stopRoutes",
    type: "POST",
    data: {
      stopID: stop_id
    },
    timeout: TIMEOUT,
    cache: false,

    success: (res) => {
      $('#routeModal').modal('show');

      response = JSON.parse("[" + res + "]")

      if (response[0].length !== 0) {
        for (i = 0; i < response[0].length; i++) {
          $("#routeTableContent").append(
            `<tr>
              <td><a onclick="getRouteTrips('${stop_id}', '${response[0][i].route_id}');">${response[0][i].route_id}</a></td>
              <td>${response[0][i].route_short_name}</td>
              <td>${response[0][i].route_long_name}</td>
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

function getRouteTrips(stop_id, route_id) {
  $('#routeTripTableContent').empty();

  $.ajax({
    url: "/stopTrips",
    type: "POST",
    data: {
      stopID: stop_id,
      routeID: route_id
    },
    timeout: TIMEOUT,
    cache: false,

    success: (res) => {
      $('#routeTripModal').modal('show');

      response = JSON.parse("[" + res + "]");

      if (response[0].length !== 0) {
        for (i = 0; i < response[0].length; i++) {
          $("#routeTripTableContent").append(
            `<tr>
              <td>${response[0][i].trip_id}</td>
              <td>${response[0][i].trip_headsign}</td>
              <td>${response[0][i].service_id}</td>
              <td><a onclick="getDates('${response[0][i].trip_id}');">Päivämäärät</a></td>
              <td>${response[0][i].arrival_time}</td>
              <td>${response[0][i].departure_time}</td>
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
