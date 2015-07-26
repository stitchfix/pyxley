var timeFormat = d3.time.format("%I:%M %p %a %Y");

var TwoAxisLinePlot = React.createClass({displayName: 'TwoAxisLinePlot',
    getDefaultProps: function() {
        return {
            url: "",
            chartid: "chart",
            colors: React.PropTypes.array,
            margin: {top: 30, right: 60, bottom: 50, left: 70},
            labels: {xAxis: "", yAxis1: "", yAxis2: ""},
            limits: {yAxis1: null, yAxis2: null}
        };
    },
    getInitialState: function() {
        return {
            chart: null
        };
    },
    componentDidMount: function() {
        this.setState({chart: this._initGraph(this.state.chart)});
    },
    _initGraph: function(chart) {
        chart = twoAxisFocusChart()
            .margin(this.props.margin)
            .color(this.props.colors);

        chart.lines1.interpolate('monotone');
        chart.lines2.interpolate('monotone');
        chart.linesC.interpolate('monotone');

        chart.xAxis
            .showMaxMin(false)
            .tickFormat(function(d){return d3.time.format('%X')(new Date(d));});

        chart.xCAxis
            .showMaxMin(false)
            .tickFormat(function(d){return d3.time.format('%X')(new Date(d));});

        chart.y1Axis
            .axisLabel(this.props.labels.yAxis1)
            .tickFormat(d3.format(',.2f'));

        chart.y2Axis
            .axisLabel(this.props.labels.yAxis2)
            .tickFormat(d3.format(',.2f'));

        chart.yCAxis
            .tickFormat(d3.format(',.2f'));

        var sig = 5;
        d3.json(this.props.url,
            function(error, result) {
                result.data.forEach(function(d){
                    d.values.forEach(function(v){
                        v.x = new Date(v.x * 1000);
                    });
                });
                var sval = result.yAxis1.std;
                var mval = result.yAxis1.mean;
                chart.yDomain1([0, mval + sig*sval]);

                var sval = result.yAxis2.std;
                var mval = result.yAxis2.mean;
                chart.yDomain2([0, mval + sig*sval]);
                chart.yDomainC([0, mval + 3*sval]);

                var svg = d3.select("#".concat(this.props.chartid, " svg"))
                    .datum(result.data)
                    .call(chart);
            }.bind(this));

        nv.utils.windowResize(function() { chart.update() });

        return chart;
    },
    update: function(params) {

        var sig = 5;
        d3.json(this.props.url.concat("?", $.param(params)),
            function(error, result) {
                result.data.forEach(function(d){
                    d.values.forEach(function(v){
                        v.x = new Date(v.x * 1000);
                    });
                });

                var sval = result.yAxis1.std;
                var mval = result.yAxis1.mean;
                this.state.chart.yDomain1([0, mval + sig*sval]);

                var sval = result.yAxis2.std;
                var mval = result.yAxis2.mean;
                this.state.chart.yDomain2([0, mval + sig*sval]);
                this.state.chart.yDomainC([0, mval + 3*sval]);

                var svg = d3.select("#".concat(this.props.chartid, " svg"))
                    .datum(result.data)
                    .transition()
                    .duration(500)
                    .call(this.state.chart);
                nv.utils.windowResize(function() { this.state.chart.update() });

        }.bind(this));
    },
    render: function() {
        return (
            React.createElement("div", null, 
            React.createElement("h2", null, this.props.title), 
            React.createElement("div", {id: this.props.chartid}, React.createElement("svg", null))
            )
        );
    }
});

module.exports.TwoAxisLinePlot = TwoAxisLinePlot;