
import React from 'react';
import ReactDOM from 'react-dom';
import {Navs} from 'pyxley';
import {ChartManager} from './chartmanager';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            layouts: [],
            navlinks: [],
            brand: ""
        };
    }

    get_layout() {
        let path = window.location.pathname.replace("/", "");
        path = path.length > 0 ? path : "antiquing";
        $.get(this.props.url.concat(path, "/"), function(result){
            this.setState({
                layouts: result.layouts
            })
        }.bind(this));
    }

    get_paths() {
        $.get(this.props.url, function(result){
            this.setState({
                navlinks: result.navlinks,
                brand: result.brand
            })
        }.bind(this));
    }

    componentWillMount() {
        this.get_layout();
        this.get_paths();
    }

    render() {

        const {children} = this.props
        const child = children && React.cloneElement(
            React.Children.only(children),
            this.state
        )

        return (
            <div>
            <Navs navlinks={this.state.navlinks} brand={this.state.brand} />
            <div className="container">{child}</div>
            </div>
        )

    }
}

App.defaultProps = {
    url: "/api/props/"
}

ReactDOM.render(
  <App>
    <ChartManager />
  </App>,
  document.getElementById("component_id")
);
