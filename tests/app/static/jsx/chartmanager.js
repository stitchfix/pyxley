import React from 'react';
import {Row} from 'react-bootstrap';
import {PyxleyChart} from './pyxleychart';

class ChartManager extends React.Component {

    constructor(props){
        super(props);
    }

    render() {
        let components = [];
        if (this.props.layouts.length > 0) {
            components = this.props.layouts.map(function(x, index) {
                return (
                    <Row key={'chart_row_'.concat(index)}>
                    <h1>{x.title}</h1>
                    <PyxleyChart
                        id={'pyxley_chart_'.concat(index)}
                        key={'pyxley_chart_'.concat(index)}
                        filters={x.filters}
                        charts={x.charts} />
                    <br/>
                    </Row>

                );
            }.bind(this));
        }

        return (
            <div id={'chart_manager_base'}>
                {components}
            </div>
        );
    }

};

export {ChartManager};
