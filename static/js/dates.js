
function getDates(trip_id) {
  $.ajax({
    url: "/tripDates",
    type: "POST",
    data: { tripID: trip_id },
    timeout: TIMEOUT,
    cache: false,

    success: (res) => {
      response = JSON.parse("[" + res + "]");

      if (response[0].length !== 0) {
        $('#calendarModal').modal('show');
        $('#calendarModalBody').empty();

        var firstYear = moment(response[0][0].date).get('year'); var firstMonth = moment(response[0][0].date).get('month') + 1;
        var lastYear = moment(response[0][response[0].length - 1].date).get('year'); var lastMonth = moment(response[0][response[0].length - 1].date).get('month') + 1;
        var dayNames = ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su'];
        var monthNames = ['Tammikuu', 'Helmikuu', 'Maaliskuu', 'Huuhtikuu', 'Toukokuu', 'Kesäkuu', 'Heinäkuu', 'Elokuu', 'Syyskuu', 'Lokakuu', 'Marraskuu', 'Joulukuu'];
        var table = document.getElementById('calendarModalBody');

        for (year = 0; year <= (lastYear - firstYear); year++) {
          table.innerHTML += `<table id="calendarTable"><thead id="calendarHead${year}"></thead><tbody id="calendarBody${year}"></tbody></table>`

          $(`#calendarHead${year}`).append(
            `<tr id="${firstYear + year}"><th id="headInfo">${firstYear + year}</th></tr>`
          )

          for (j = 0; j < 38; j++) {
            $(`#${firstYear + year}`).append(`<th>${dayNames[j % dayNames.length]}</th>`)
          }

          for (m = firstMonth - 1; m < lastMonth; m++) {
            var currentMonth = moment().year(firstYear + year).month(m);
            var monthDates = response[0].filter((date) => {
              var currentDate = moment(date.date);
              if (currentDate >= currentMonth.startOf('month') && currentDate <= currentMonth.endOf('month')) {
                return true;
              }

              return false;
            });

            if (monthDates.length !== 0) {
              $(`#calendarBody${year}`).append(`<tr id="${m}${year}"><td id="bodyInfo">${monthNames[m]}</td></tr>`)

              var offCount = 0;
              for (i = 1; i < 39; ) {
                if (i >= currentMonth.startOf('month').day() && i <= (currentMonth.endOf('month').get('date') + offCount)) {
                  foundCount = 0;
                  for (j = 0; j < monthDates.length; j++) {
                    var date = moment(monthDates[j].date).format('YYYY-MM-DD');
                    var cdate = moment(currentMonth.date(i - offCount)).format('YYYY-MM-DD');

                    if (moment(date).isSame(cdate)) {
                      $(`#${m}${year}`).append(`<td id="markedDate">${i - offCount + foundCount}</td>`)
                      foundCount++;
                      i++
                      break;
                    }
                  }

                  if (foundCount === 0) {
                    $(`#${m}${year}`).append(`<td id="unMarkedDate">${i - offCount}</td>`)
                    i++;
                  }
                } else {
                  $(`#${m}${year}`).append(`<td id="blank"></td>`)
                  offCount++;
                  i++;
                }
              } // end of for day
            } // end of if

          } // end of for month
        } // end of for year
      } else {
        $('#calendarModal').modal('hide');
        alert('Reitin aikoja ei löytynyt!');
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
