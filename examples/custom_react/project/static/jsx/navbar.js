
import {Navbar, NavItem, Nav} from 'react-bootstrap';
import React from 'react';
import ReactDOM from 'react-dom';

const navbarInstance = (
    <Navbar inverse>
        <Navbar.Header>
        <Navbar.Brand>Pyxley</Navbar.Brand>
        </Navbar.Header>
        <Nav pullRight eventKey={0}></Nav>
    </Navbar>
);

ReactDOM.render(navbarInstance, document.getElementById('navbarid'));
