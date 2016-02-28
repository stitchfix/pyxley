
import {Navbar, NavItem, Nav} from 'react-bootstrap';
import React from 'react';
import ReactDOM from 'react-dom';

const navbarInstance = (
    <Navbar brand="Pyxley" inverse toggleNavKey={0}>
    <Nav right eventKey={0}>
    </Nav>
    </Navbar>
);

ReactDOM.render(navbarInstance, document.getElementById('navbarid'));
