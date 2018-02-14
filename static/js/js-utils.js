$(document).ready(function() {
    getPrices();
});

/*setInterval(function() {
   getPrices();
}, 60000);*/

function getPrices(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var ctx = document.getElementById("btc_eth_pc");
            var ctx_p = document.getElementById("price_btc");
            var ctx_e = document.getElementById("price_eth");
            var resp = JSON.parse(this.responseText);

            /*console.log(resp['data']['datasets'][1]['data'])*/

            var perc_change = new Chart(ctx, {
                 type: 'line',
                 data: {
                     labels: resp['data']['labels'],
                     datasets: [{
                        label: resp['data']['datasets'][0]['label'],
                        data: resp['data']['datasets'][0]['data']['change'],
                        lineTension: 0,
                        backgroundColor: 'transparent',
                        borderColor: '#FFBF00',
                        borderWidth: 1,
                        pointBackgroundColor: '#FFBF00'
                     },{
                        label: resp['data']['datasets'][1]['label'],
                        data: resp['data']['datasets'][1]['data']['change'],
                        lineTension: 0,
                        backgroundColor: 'transparent',
                        borderColor: '#2E9AFE',
                        borderWidth: 1,
                        pointBackgroundColor: '#2E9AFE'
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
                    display: true,
                    labelString: "BTC-ETH",
                    }
                }
             });

            var price_btc = new Chart(ctx_p, {
                 type: 'line',
                 data: {
                     labels: resp['data']['labels'],
                     datasets: [{
                        label: resp['data']['datasets'][0]['label'],
                        data: resp['data']['datasets'][0]['data']['price'],
                        lineTension: 0,
                        backgroundColor: 'transparent',
                        borderColor: '#FFBF00',
                        borderWidth: 1,
                        pointBackgroundColor: '#FFBF00'
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
                    display: true,
                    labelString: "BTC-ETH",
                    }
                }
             });

            var price_eth = new Chart(ctx_e, {
                 type: 'line',
                 data: {
                     labels: resp['data']['labels'],
                     datasets: [{
                        label: resp['data']['datasets'][1]['label'],
                        data: resp['data']['datasets'][1]['data']['price'],
                        lineTension: 0,
                        backgroundColor: 'transparent',
                        borderColor: '#2E9AFE',
                        borderWidth: 1,
                        pointBackgroundColor: '#2E9AFE'
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
                    display: true,
                    labelString: "BTC-ETH",
                    }
                }
             });
        }
    };
    xhttp.open("GET", "/prices", true);
    xhttp.send();
}

