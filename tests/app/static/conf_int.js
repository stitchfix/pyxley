const confidence_interval = function(data, chartid) {
        if (data.length > 0) {

            var minMin = data[0][0];
            var maxMax = data[0][3];

            var x = d3.scale.linear()
                .domain([minMin, maxMax])
                .range([56, 156]);

            var ciCells = d3.selectAll("#" + chartid + " g")
                .data(data)
                .attr("transform", function(d) { return "translate(" + (x(d[1]) + 28) + ", 0)"; });

            ciCells.append("rect")
                .attr("height", 20)
                .attr("fill", "steelBlue")
                .attr("rx", 4)
                .attr("ry", 4)
                .attr("width", function(d) { return x(d[2]) - x(d[1]); });

            var dollar = d3.format(".3n");
            var lbText = ciCells.append("text")
                .attr("y", 10)
                .attr("dy", ".35em")
                .attr("font-size", 12)
                .attr("fill", "white")
                .text(function(d) { return dollar(d[1]/1000) + "k"; })

            var ubText = ciCells.append("text")
                .attr("y", 10)
                .attr("dy", ".35em")
                .attr("font-size", 12)
                .attr("fill", "white")
                .text(function(d) { return dollar(d[2]/1000) + "k"; })

            lbText
                .attr("fill", function(d) {
                    if (x(d[2]) - x(d[1]) > 58.8) {
                        return "white";
                    } else {
                        return "steelBlue";
                    }
                })
                .attr("x", function(d) {
                    if (x(d[2]) - x(d[1]) > 58.8) {
                        return 4;
                    } else {
                        return 0.0 - this.getBBox().width - 4;
                    }
                });

            ubText
                .attr("fill", function(d) {
                    if (x(d[2]) - x(d[1]) > 58.8) {
                        return "white";
                    } else {
                        return "steelBlue";
                    }
                })
                .attr("x", function(d) {
                    if (x(d[2]) - x(d[1]) > 58.8) {
                        return x(d[2]) - x(d[1]) - this.getBBox().width - 4;
                    } else {
                        return x(d[2]) - x(d[1]) + 4;
                    }
                });

        }
    };