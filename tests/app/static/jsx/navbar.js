
import {Navbar, NavItem, Nav} from 'react-bootstrap';
import React from 'react';
import ReactDOM from 'react-dom';

class Navs extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            pages: []
        };
    }

    componentWillMount() {
        let url = "/api/props/";
        $.get(url, function(result){
            this.setState({
                pages: result.pages
            })
        }.bind(this));
    }

    render() {
        return (
            <Navbar>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href='#'>Tests</a>
                    </Navbar.Brand>
                </Navbar.Header>
                <Nav pullRight>
                   <NavItem eventKey={1} href="filters">Filters</NavItem>
                   <NavItem eventKey={1} href="mg">metrics-graphics</NavItem>
                   <NavItem eventKey={1} href="plotly">Plotly</NavItem>
                </Nav>
            </Navbar>
        )
    }
}
// export {Navs};

ReactDOM.render(
  <Navs/>,
  document.getElementById("nav_bar_id")
);
