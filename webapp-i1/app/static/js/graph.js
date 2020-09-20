google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
google.charts.load('current', {'packages':['gauge']});

function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ['Days', 'Prediction 2020', 'Actual 2020', 'Actual 2019' ],
    ['Monday',  90,      96,     136],
    ['Tuesday',  92,      96,     138],
    ['Wednesday',  102,     104,    139],
    ['Thursday',  91,      94,     132],
    ['Friday',  95,      93,     116],
    ['Saturday',  79,      76,     79],
    ['Sunday',  86,      86,     93]

  ]);
  var options = {
    title: 'Customer potential',
    curveType: 'function',
    legend: { position: 'bottom' }
  };

  var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

  chart.draw(data, options);
}


