zingchart.render({
    id: "ohlcv-chart",
    data: {
        "type": "stock",
        "title": {
            "text": "Candlestick Chart"
        },
        "plot": {
            "aspect": "candlestick"
        },
        "scale-y": {
            "values": candle_range
        },
        "series": [
            {
                "values": candle_data
            }]
    }
});
