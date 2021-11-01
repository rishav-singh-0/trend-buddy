const chart = LightweightCharts.createChart(document.getElementById("chart"), { width: 600, height: 400 });
const candlestickSeries = chart.addCandlestickSeries();

fetch('http://127.0.0.1:8000/data/candle/BTCUSDT')
    .then((r) => r.json())
    .then((response) => (
        // console.log(response)
        candlestickSeries.setData(response)
    ))