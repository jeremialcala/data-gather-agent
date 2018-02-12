$(document).ready(function() {
    var req = new XMLHttpRequest();
    req.open('GET', document.location, false);
    req.send(null);
    var sessionid = req.getResponseHeader("X-Session");
    getPrices();
    document.getElementById("my-session").value = sessionid;
});

function getPrices(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var ctx = document.getElementById("myChart");
            var resp = JSON.parse(this.responseText);
            var myChart = new Chart(ctx, {
                 type: 'line',
                 data: {
                     labels: resp['data']['labels'],
                     datasets: [{
                        data: resp['data']['dataset'],
                        lineTension: 0,
                        backgroundColor: 'transparent',
                        borderColor: '#007bff',
                        borderWidth: 4,
                        pointBackgroundColor: '#007bff'
                     }],
                 },
                 options: {
                    scales: {
                    yAxes: [{
                      ticks: {
                        beginAtZero: false
                      }
                    }]
                    },
                    legend: {
                    display: false,
                    }
                }
             });

        }
    };
    xhttp.open("GET", "/prices", true);
    xhttp.send();
}

