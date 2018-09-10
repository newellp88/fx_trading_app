var context = document.getElementById('lineGraph').getContext('2d');
console.log(context)

var lineGraph = new Chart (context, {
    type: "line",
    data: data
});