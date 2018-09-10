zingchart.render({
    id: 'lineChart',
    data: {
        type: 'line',
        series: [{
            values: data
        }]}
    });

zingchart.render({
    id: 'data-table',
    data: {
        type: 'grid',
        series: [
            {
                "values":[1,"Jon","Anderson","January 9, 1957","M","United Kingdom"]
            },
            {
                "values":[2,"Steve","Hogarth","January 25, 1950","M","United Kingdom"]
            },
            {
                "values":[3,"Jim","Carrey","June 12, 1972","M","United States"]
            },
            {
                "values":[4,"Paul","Hogan","October 22, 1956","M","Australia"]
            },
            {
                "values":[5,"Margaret","Thatcher","January 27, 1937","F","United Kingdom"]
            }
        ]
    }
});

zingchart.render({
    id: 'summary-table',
    data: {
        type: 'grid',
        series: [
            {
                "values":[1,"Jon","Anderson","January 9, 1957","M","United Kingdom"]
            },
            {
                "values":[2,"Steve","Hogarth","January 25, 1950","M","United Kingdom"]
            },
            {
                "values":[3,"Jim","Carrey","June 12, 1972","M","United States"]
            },
            {
                "values":[4,"Paul","Hogan","October 22, 1956","M","Australia"]
            },
            {
                "values":[5,"Margaret","Thatcher","January 27, 1937","F","United Kingdom"]
            }
        ]
    }
});

zingchart.render({
    id: "heatmap",
    data: {
        "type": "heatmap",
        "scale-y": {
            "mirrored": true    //Flips data so that rows appear from top to bottom.
        },
        "series": [
            {"values": [59,15,5,30,60,99,28]},
            {"values": [34,32,87,65,9,17,40]},
            {"values": [90,19,50,39,12,49,14]}
        ]
    }
});
