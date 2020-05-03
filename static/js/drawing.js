// D functions

var D = {
    svg: null,
    padding: 10,
    scale: 1.5,
    width: 0,
    height: 0,
}

function setup() {
    D.width = Math.max(960, innerWidth),
    D.height = Math.max(500, innerHeight);

    D.svg = d3.select("body").append("svg")
                                   .attr("width", D.width)
                                   .attr("height", D.height);
}

function drawGameObject(o, idx) {
    var id = "location" + o.id
    var brand = brands[o.brand_id]
    var image = templates[o.type]["image"]
    var w = templates[o.type]["width"]
    var h = templates[o.type]["height"]
    // Brand indicator rect
    D.svg.append("rect")
        .attr("class", "game_object")
        .attr('x', idx*(D.scale*w)+D.padding)
        .attr('y', 10)
        .attr('width', w)
        .attr('height', h+D.padding)
        .attr('stroke', brand.colour)

    // Location image
    D.svg.append("image")
        .attr("id", id)
        .attr("xlink:href", image)
        .attr('x', idx*(D.scale*w)+D.padding)
        .attr('y', D.padding*D.scale)
        .attr('width', w)
        .attr('height', h)

    // Create a tooltip
    var tt = d3.select("body")
      .append("div")
        .style("position", "absolute")
        .style("visibility", "hidden")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "1px")
        .style("border-radius", "5px")
        .style("padding", "10px")
        .html(function() {
            var content = "<p><h4>" + brand.name + " " + o.name + "</h4><hr />"
            var keys = Object.keys(o.stats)
            keys.forEach(function(v, i) {
                content = content + o.stats[v].label + ": " + o.stats[v].value + "<br />"
            });
            content = content + "</p>"

            return content
        });

    d3.select("#" + id)
        .on("mouseover", function(){return tt.style("visibility", "visible");})
        .on("mousemove", function(){return tt.style("top", (event.pageY)+"px").style("left",(event.pageX)+"px");})
        .on("mouseout", function(){return tt.style("visibility", "hidden");});
}

