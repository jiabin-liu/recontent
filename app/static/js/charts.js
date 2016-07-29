queue()
    .defer(d3.json, "/data/alltime")
    .await(makeGraphs);


function makeGraphs(error, dataJson) {
  'use strict';
  // Grab the data
	var data = dataJson;
  // Now count the number of times a corpus was requested.
  var counts = [];
  data.forEach(function(d){
    var corpusname = d["corpus"];
    if (typeof counts[corpusname] === 'undefined') {
      counts[corpusname] = 0;
    }
    counts[corpusname]++;
  })
  // The data now looks like this:
  // [speechwiki: 1, simple-wiki: 67, speech: 10]
  // We need to change it into a list of arrays of key value pairs
  var dataset = [];
  for (var x in counts) {
    dataset.push({'label': x, 'count': counts[x]})
  }
  // Time for the plotting magic
  var width = 300;
  var height = 300;
  var radius = Math.min(width, height) / 2;
  var donutWidth = 50;
  var legendRectSize = 18;
  var legendSpacing = 4;
  var color = d3.scale.category10();

  var svg = d3.select('#piechart')
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', 'translate(' + (width / 2) +
      ',' + (height / 2) + ')');

  var arc = d3.svg.arc()
    .innerRadius(radius - donutWidth)
    .outerRadius(radius);

  var pie = d3.layout.pie()
    .value(function(d) { return d.count; })
    .sort(null);

  var path = svg.selectAll('path')
    .data(pie(dataset))
    .enter()
    .append('path')
    .attr('d', arc)
    .attr('fill', function(d, i) {
      return color(d.data.label);
    });

  var legend = svg.selectAll('.legend')
    .data(color.domain())
    .enter()
    .append('g')
    .attr('class', 'legend')
    .attr('transform', function(d, i) {
      var height = legendRectSize + legendSpacing;
      var offset =  height * color.domain().length / 2;
      var horz = -2 * legendRectSize;
      var vert = i * height - offset;
      return 'translate(' + horz + ',' + vert + ')';
    });

  legend.append('rect')
    .attr('width', legendRectSize)
    .attr('height', legendRectSize)
    .style('fill', color)
    .style('stroke', color);

  legend.append('text')
    .attr('x', legendRectSize + legendSpacing)
    .attr('y', legendRectSize - legendSpacing)
    .text(function(d) { return d; });

  var tooltip = d3.select('#piechart')
    .append('div')
    .attr('class', 'tooltip');
  tooltip.append('div')
    .attr('class', 'label');
  tooltip.append('div')
    .attr('class', 'count');
  tooltip.append('div')
    .attr('class', 'percent');


  path.on('mouseover', function(d) {
    var total = d3.sum(dataset.map(function(d) {
      return d.count;
    }));
    var percent = Math.round(1000 * d.data.count / total) / 10;
    console.log( percent, d.data.label, d.data.count)
    tooltip.select('.label').html(d.data.label);
    tooltip.select('.count').html(d.data.count);
    tooltip.select('.percent').html(percent + '%');
    tooltip.style('display', 'block');
  });
  path.on('mouseout', function() {
    tooltip.style('display', 'none');
  });

};
