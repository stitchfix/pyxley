import React from 'react';
import {Row, Col} from 'react-bootstrap';
import {Filter, Chart} from 'pyxley';


class PyxleyChart extends React.Component {
    constructor(props) {
        super(props);
    }

    _gatherParams(input) {
        var params = {};

        for(var i = 0; i < this.props.filters.length; i++){
            let fidx = 'filter_'.concat(i);
            let vals = this.refs[fidx].refs.filter.getCurrentState();

            for(var key in vals){
                params[key] = vals[key];
            }
        }
        if(input){
            for(var i = 0; i < input.length; i++){
                params[input[i].alias] = input[i].value;
            }
        }
        return params;
    }

    _handleClick(input) {
        // update the charts
        var params = this._gatherParams(input);
        for(var i = 0; i < this.props.charts.length; i++){
            this.refs['chart_'.concat(i)].update(params);
        }


        for(var i = 0; i < this.props.filters.length; i++){
            let fidx = 'filter_'.concat(i)
            if(typeof this.refs[fidx].refs.filter.update === 'function') {
                this.refs[fidx].refs.filter.update(params);
            }
        }
        return params;
    }


    get_filters(prop_filters) {
        let filters = [];
        if (prop_filters.length > 0) {
            filters = prop_filters.map(function(x, index){
                return (
                    <div>
                    {x.label ? <h2>{x.label}</h2> : null}
                    <Filter
                        ref={'filter_'.concat(index)}
                        id={'filter_'.concat(index)}
                        onChange={this._handleClick.bind(this)}
                        dynamic={true}
                        type={x.type}
                        options={x.options}/>
                    <br/>
                    </div>
                );
            }.bind(this));
        }
        return filters;
    }

    get_charts(prop_charts) {
        let charts = [];
        if(prop_charts.length > 0){
            charts = prop_charts.map(function(x, index){
                return(
                    <Chart
                        ref={'chart_'.concat(index)}
                        id={"chart_".concat(index)}
                        type={x.type}
                        options={x.options}/>
                    );
            });
        }
        return charts;
    }

    render(){

        let filters = this.get_filters(this.props.filters);
        let charts = this.get_charts(this.props.charts);

        return (
            <div>
                <Col xs={6} md={2}>
                    {filters}
                </Col>

                <Col xs={12} md={10}>
                    {charts}
                </Col>
            </div>
            );
    }

}

PyxleyChart.contextTypes = {
    router: React.PropTypes.object
};
export {PyxleyChart};
