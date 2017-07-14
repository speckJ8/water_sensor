(() => {

    var waterLevelChart,
        waterLevelChartOptions = {
        chart: {
            title: 'Volume de água no reservatório',
            subltitle: 'em metros cúbicos'
        },
        //curveType: 'function' // to show a smooth curve
    }

    /**
     * Load initial values in the charts
     */
    drawCharts = () => {
        waterLevelChart = new google.charts.Line(
            document.getElementById('reservoir-water-level-chart'))
        var today     = new Date();            
        var yesterday = new Date(today.getTime() - 25*60*60*1000);
        var todayStr = today.getFullYear() + '-' + 
            (today.getMonth() > 9 ? today.getMonth() : "0" + today.getMonth()) + '-' + 
            (today.getDate() > 9 ? today.getDate() : "0" + today.getDate());
        var yestStr  = yesterday.getFullYear() + '-' + 
            (yesterday.getMonth() > 9 ? yesterday.getMonth() : "0" + yesterday.getMonth()) + '-' + 
            (yesterday.getDate() > 9 ? yesterday.getDate() : "0" + yesterday.getDate());
        
        drawChart('waterLevel', 'day', yestStr, todayStr);
    }

    /**
     * Draw new data in a chart
     * @param data the type of data to get (pH or salinity ...)
     * @param filter to filter the data to show
     */
    drawChart = (data, clusterBy, from, until) => {
        var url = RESERVOIR_INFO_PATH + "?data=" + data +
            "&dateFrom=" + from + "&dateUnitl=" + until + 
            "&clusterBy=" + clusterBy;

        $.get(url)
        .done((result) => {

            jsonRes = JSON.parse(result); // should be a list of measurements
            var chartData = new google.visualization.DataTable();
            switch (data) {
            case 'waterLevel':
                // x axis label according to the grouping
                if (clusterBy == 'day') 
                    chartData.addColumn('number', 'Dia');
                else if (clusterBy == 'month')
                    chartData.addColumn('number', 'Mês');
                else chartData.addColumn('number', 'Hora');

                chartData.addColumn('number', 'Volume de Água');
                for (var measurement in jsonRes) {
                    chartData.addRow([measurement[clusterBy], measurement['waterLevel']]);
                }

                waterLevelChart.draw(chartData, google.charts.Line.convertOptions(waterLevelChartOptions));
                break;
            default:
                console.log('data = ' + data);
            }
        })
        .fail(() => {
            console.log('fail');
        })
    }

    /* load google charts API */
    google.charts.load('current', { 'packages': ['line'] });
    google.charts.setOnLoadCallback(drawCharts);

})();