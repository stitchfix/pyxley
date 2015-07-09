var Navbar = ReactBootstrap.Navbar;
var NavItem = ReactBootstrap.NavItem;
var Nav = ReactBootstrap.Nav;

const navbarInstance = (
    <Navbar brand="Pyxley" inverse toggleNavKey={0}>
    <Nav right eventKey={0}>
    </Nav>
    </Navbar>
);

React.render(navbarInstance, document.getElementById('navbarid'));