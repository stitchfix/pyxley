
import {Navbar, NavItem, Nav} from 'react-bootstrap';
import {LinkContainer} from 'react-router-bootstrap';
import React from 'react';
import ReactDOM from 'react-dom';

class Navs extends React.Component {
    render() {
        return (
            <Navbar>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href='#'>Tests</a>
                    </Navbar.Brand>
                </Navbar.Header>
                <Nav pullRight>
                   <LinkContainer to={{pathname: "/"}}>
                       <NavItem eventKey={1}>Charts</NavItem>
                   </LinkContainer>
                </Nav>
            </Navbar>
        )
    }
}
export {Navs};
