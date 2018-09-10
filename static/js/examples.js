zingchart.render({
    id: "ohlcv-chart",
    data: {
        type: "stock",
        "scale-y": "0.9:1.8:0.1",
        plot: {
            aspect: "candlestick"
        },
        series: [{
            values: candle_data
        }]
    }
});
/*
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
*/

/*
// plot not populating for some reason
zingchart.render({
    id: "ohlcv-chart",
    data: {
    "type":"stock",
    "title":{
    "text": "Price Chart",
        "font-family":"Garamond"
},
"subtitle":{
    "text":"Source: Oanda.com",
        "font-weight":"normal"
},
"plot":{
    "aspect":"candlestick",
        "tooltip":{
        "visible":false
    },
    "trend-up":{
        "line-color":"#0066ff"
    },
    "trend-down":{
        "line-color":"#ff3300"
    },
    "preview":{
        "type":"area", //area (default) or line
            "line-color":"#0099ff",
            "background-color":"#0099ff"
    }
},
"scale-x":{
    "min-value":1438592400000, //08/03/15
        "step":"day",
        "transform":{
        "type":"date",
            "all":"%D,<br>%M %d"
    },
    "max-items":10,
        "item":{
        "font-size":10
    },
    "zooming":true,
    //"zoom-to-values":[1448960400000,1454058000000]
},
"crosshair-x":{
    "plot-label":{
        "text":"Open: $%v0<br>High: $%v1<br>Low: $%v2<br>Close: $%v3",
            "decimals":2
    },
    "scale-label":{
        "text":"%v",
            "transform":{
            "type":"date",
                "all":"%D,<br>%M %d, %Y"
        }
    }
},
"preview":{

},
"scale-y":{
    "values":candle_range,
        "format":"$%v",
        "item":{
        "font-size":10
    },
    "guide":{
        "line-style":"solid"
    }
},
"crosshair-y": {
    "type": "multiple", //"single" (default) or "multiple"
        "scale-label": {
        "visible": false
    }
},
"plotarea":{
    "margin-top":"15%",
        "margin-bottom":"25%"
},
"series":[{
        "values": candle_data
    }]
    }
});
*/
/*
// mixed chart works, but volume/price scale doesn't
zingchart.render({
    id: 'ohlcv-chart',
    data: {
        type: "mixed",
        "scale-y": candle_range,
        "scale-y-2": volume_range,
        series: [{
            type: "stock",
            scales: "scale-x,scale-y",
            values: candle_data // candle_data == list of lists [[timestamp, [Open, High, Low, Close]]]
        }, {
            type: "bar",
            scales: "scale-x,scale-y-2",
            values: volume_data // simple list is fine
        }]
    }});
*/