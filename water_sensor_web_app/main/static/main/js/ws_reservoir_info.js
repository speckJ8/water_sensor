$(document).ready(() => {

    /* to specify the range of data to read */
    var fromField = document.getElementById('dateFrom');
    var untilField = document.getElementById('dateUnitl');

    var waterLevelChart,
        waterLevelChartOptions = {
            chart: {
                title: 'Altura do nível de água no reservatório',
                subtitle: 'em metros (m)'
            },
            colors: ['blue']
    }

    var salinityChart,
        salinityChartOptions = {
            chart: {
                title: 'Salinidade da Água',
                subtitle: 'em gramas de sal por kilogramas de água (PSU)'
            },
            colors: ['#808080']
        }

    var conductivityChart,
        conductivityChartOptions = {
            chart: {
                title: 'Condutividade da Água',
                subtitle: 'em micro Siemens (µS)'
            },
            colors: ['orange']
        }

    var pHChart,
        pHChartOptions = {
            chart: {
                title: 'pH da Água'
            },
            colors: ['green']
        }

    var tdsChart,
        tdsChartOptions = {
            chart: {
                title: 'Total de Sólidos Disolvidos na Água',
                subtitle: 'em partes por millão (ppm)'
            },
            colors: ['#423f38']
        }


    /**
     * To load the data into the charts
     */
    loadChartsValues = () => {
        var from  = fromField.value;
        var until = untilField.value;

        var grouping = 'hour';
        // TODO: define the grouping

        drawChart('waterLevel', grouping, from, until);
        drawChart('salinity', grouping, from, until);
        drawChart('conductivity', grouping, from, until);
        drawChart('pH', grouping, from, until);
        drawChart('tds', grouping, from, until);
    }

    /**
     * Load initial values in the charts
     */
    drawCharts = () => {

        waterLevelChart = new google.charts.Line(
            document.getElementById('reservoir-water-level-chart'));
        salinityChart = new google.charts.Line(
            document.getElementById('reservoir-salinity-chart'));
        conductivityChart = new google.charts.Line(
            document.getElementById('reservoir-conductivity-chart'));
        pHChart = new google.charts.Line(
            document.getElementById('reservoir-pH-chart'));
        tdsChart = new google.charts.Line(
            document.getElementById('reservoir-tds-chart'));

        var today = new Date();
        var yesterday = new Date(today.getTime() - 25*60*60*1000);

        // initially load only today's data
        fromField.value  = yesterday.getFullYear() + '-' +
            (yesterday.getMonth() > 8 ? (yesterday.getMonth()+1) : "0" + (yesterday.getMonth()+1)) + '-' +
            (yesterday.getDate() > 9 ? yesterday.getDate() : "0" + yesterday.getDate());;
        untilField.value = today.getFullYear() + '-' +
            (today.getMonth() > 8 ? (today.getMonth()+1) : "0" + (today.getMonth()+1)) + '-' +
            (today.getDate() > 9 ? today.getDate() : "0" + today.getDate());;
        // for when the values change
        fromField.onchange = untilField.onchange = loadChartsValues;

        // load chart values for the first time
        loadChartsValues();
    }

    /**
     * Draw new data in a chart
     * @param {string} data the type of data to get (pH or salinity ...)
     * @param {string} clusterBy how to group the data (by hour, day or month)
     * @param {string} from all the measurements should be after this date. Format yyyy-mm-dd
     * @param {string} until all the measurements should be before this date. Format yyyy-mm-dd
     */
    drawChart = (data, clusterBy, from, until) => {
        var url = RESERVOIR_INFO_PATH + "?data=" + data +
            "&dateFrom=" + from + "&dateUnitl=" + until +
            "&clusterBy=" + clusterBy;

        $.get(url)
        .done((result) => {

            jsonRes = JSON.parse(result); // should be a list of measurements

            var chartData = new google.visualization.DataTable();
            // x axis label according to the grouping
            if (clusterBy == 'day')
                chartData.addColumn('number', 'Dia');
            else if (clusterBy == 'month')
                chartData.addColumn('number', 'Mês');
            else
                chartData.addColumn('number', 'Hora');

            var chartToDraw;
            var options;
            var desc;

            switch (data) {
            case 'waterLevel':
                desc = 'Altura';
                chartToDraw = waterLevelChart;
                options = waterLevelChartOptions;
                break;
            case 'salinity':
                desc = 'Salinidade';
                chartToDraw = salinityChart;
                options = salinityChartOptions;
                break;
            case 'conductivity' :
                desc = 'Condutividade';
                chartToDraw = conductivityChart;
                options = conductivityChartOptions;
                break;
            case 'pH' :
                desc = 'pH';
                chartToDraw = pHChart;
                options = pHChartOptions;
                break;
            case 'tds' :
                desc = 'TDS';
                chartToDraw = tdsChart;
                options = tdsChartOptions;
                break;
            default:
                Util.showMsgDialog('Gráfico', 'Tipo de dados desconhecido');
                return;
            }

            chartData.addColumn('number', desc);

            for (var m in jsonRes) {
                var measurement = jsonRes[m];
                chartData.addRow([measurement[clusterBy], measurement[data]]);
                console.log('x_val = ' + measurement[clusterBy]);
            }

            chartToDraw.draw(chartData, google.charts.Line.convertOptions(options));

        })
        .fail(() => {
            console.log('fail');
        })
    }

    /* load google charts API */
    google.charts.load('current', { 'packages': ['line'] });
    google.charts.setOnLoadCallback(drawCharts);

});
