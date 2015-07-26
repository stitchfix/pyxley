var Button = ReactBootstrap.Button;
var Filter = require('../bower_components/pyxley/build/pyxley').Filter;
var Row = ReactBootstrap.Row;
var Chart = require('./twoAxisLinePlot').TwoAxisLinePlot;

const RunLayout  = React.createClass({displayName: 'RunLayout',
    getDefaultProps: function() {
        return {
            filters: React.PropTypes.array,
            charts: React.PropTypes.array,
            dynamic: React.PropTypes.string
        };
    },
    _handleClick: function(input) {
        var params = {};
        for(var i = 0; i < this.props.filters.length; i++){
            var vals = this.refs["filter_".concat(i)].refs.filter.getCurrentState();
            for(var key in vals){
                params[key] = vals[key];
            }
        }
        if(input){
            for(var i = 0; i < input.length; i++){
                params[input[i].alias] = input[i].value;
            }
        }
        for(var i = 0; i < this.props.charts.length; i++){
            this.refs["chart_".concat(i)].update(params);
        }
        return params;
    },
    render: function(){
        var items = this.props.filters.map(function(x, index){
            return(React.createElement(Filter, {
                ref: "filter_".concat(index), 
                onChange: this._handleClick, 
                dynamic: this.props.dynamic, 
                type: x.type, options: x.options}));
        }.bind(this));

        var charts = this.props.charts.map(function(x, index){
            return(React.createElement(Chart, {
                ref: "chart_".concat(index), 
                url: x.options.url, 
                chartid: x.options.chartid, 
                colors: x.options.colors}));
        });
        return (
            React.createElement("div", null, 
                React.createElement(Row, null, 
                React.createElement("div", null, 
                this.props.dynamic ? null : React.createElement(Button, {onClick: this._handleClick}, "Update!"), 
                items
                )
                ), 
                React.createElement(Row, null, 
                charts
                )
            )
            );
    }
});

module.exports.RunLayout = RunLayout;