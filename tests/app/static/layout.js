
import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, Link, browserHistory, IndexRoute } from 'react-router';
import {Navs} from './jsx/navbar';
import {ChartManager} from './jsx/chartmanager';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            layouts: []
        };
    }

    componentWillMount() {

        let url = "/api/props/";
        $.get(url, function(result){
            this.setState({
                layouts: result.layouts
            })
        }.bind(this));
    }

    render() {

        const {children} = this.props
        const child = children && React.cloneElement(
            React.Children.only(children),
            this.state
        )
        return (
            <div>
            <Navs/>
            <div className="container">{child}</div>
            </div>
        )

    }
}


ReactDOM.render(
  <Router history={ browserHistory }>
    <Route path='/' component={App}>
        <IndexRoute component={ChartManager}/>
    </Route>
  </Router>,
  document.getElementById("component_id")
);
