import React from 'react';
import {Button, Row} from 'react-bootstrap';
import {Filter} from 'pyxley';
import {TwoAxisLinePlot as Chart} from './twoAxisLinePlot';

class RunLayout extends React.Component {
    constructor(props) {
        super(props);
    }

    _handleClick(input) {
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
    }

    render() {
        var items = this.props.filters.map(function(x, index){
            return(<Filter
                ref={"filter_".concat(index)}
                onChange={this._handleClick.bind(this)}
                dynamic={this.props.dynamic}
                id={"filter_".concat(index)}
                type={x.type} options={x.options}/>);
        }.bind(this));

        var charts = this.props.charts.map(function(x, index){
            return(<Chart
                ref={"chart_".concat(index)}
                url={x.options.url}
                chartid={x.options.chartid}
                colors={x.options.colors}/>);
        });
        return (
            <div>
                <Row>
                <div>
                {this.props.dynamic ? null :
                    <Button onClick={this._handleClick.bind(this)} >Update!</Button>}
                {items}
                </div>
                </Row>
                <Row>
                {charts}
                </Row>
            </div>
            );
    }
}

export {RunLayout};
