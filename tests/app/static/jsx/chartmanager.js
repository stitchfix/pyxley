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
                    <Row>
                    <h1>{x.title}</h1>
                    <PyxleyChart
                        filters={x.filters}
                        charts={x.charts} />
                    <br/>
                    </Row>

                );
            }.bind(this));
        }

        return (
            <div>
                {components}
            </div>
        );
    }

};

export {ChartManager};
