var incomeChart = document.getElementById('incomeChart').getContext('2d');
var incomeChartData = new Chart(incomeChart, {
    type: 'line',
    data: {
        labels: ['July', 'August', 'September', 'October', 'November', 'December', 'January', 'February'],
        datasets: [{
            label: 'Gross Income',
            data: [638, 640, 780, 644, 743, 768],
            backgroundColor: 'rgba(0, 145, 189, 0.2)',
            borderWidth: 0
        }, {
            label: 'Net Earnings',
            data: [533, 556, 693, 568, 678, 696],
            backgroundColor: 'rgba(0, 189, 148, 0.2)',
            borderWidth: 0
        }, {
            label: 'Net Earnings (prediction)',
            data: [null, null, null, null, null, 768, 820, 783],
            backgroundColor: pattern.draw('dash', 'rgba(0, 0, 0, 0.08)'),
            borderWidth: 0
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: false,
                    callback: function(value, index, values) {
                        // Convert the number to a string and splite the string every 3 charaters from the end
                        value = value.toString();
                        value = value.split(/(?=(?:...)*$)/);
            
                        // Convert the array to a string and format the output
                        value = value.join('.');
                        return '$' + value;
                    }
                },
            }]
        },
        elements: {
            line: {
                cubicInterpolationMode: 'monotone'
            }
        },
        tooltips: {
            callbacks: {
                label: function (tooltipItem, data) {
                    return data['labels'][tooltipItem['index']] + ': ' + '$' + data['datasets'][0]['data'][tooltipItem['index']];
                }
            }
        },
    }
});

var csatChart = document.getElementById('csatChart').getContext('2d');
var csatChartData = new Chart(csatChart, {
    type: 'line',
    data: {
        labels: ['July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [{
            label: 'Satisfaction rate (%)',
            data: [98.6, 97.1, 98.4, 90.2, 86.4, 96.4],
            backgroundColor: 'rgba(224, 34, 85, 0.2)',
            borderWidth: 0
        }]
    },
    options: {
        tooltips: {
            callbacks: {
                label: function (tooltipItem, data) {
                    return data['labels'][tooltipItem['index']] + ': ' + data['datasets'][0]['data'][tooltipItem['index']] + '%';
                }
            }
        },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    max: 100,
                    callback: function(value, index, values) {
                        // Convert the number to a string and splite the string every 3 charaters from the end
                        value = value.toString();
                        value = value.split(/(?=(?:...)*$)/);
            
                        // Convert the array to a string and format the output
                        value = value.join('.');
                        return  value + '%';
                    }
                }
            }]
        }
    }
});