from .react_template import ReactTemplate

def get_property(x, prop):
    props = []
    for k in x:
        if prop in x[k]:
            props.append((k, x[k][prop]))
    return props

class ReactRouter(ReactTemplate):
    """Class to generate javascript for react-router.

        This class creates a jsx file for react-router and assembles
        the jsx components for several pages

        Args:
            components (dict): routes and files by component name
            element_id (str): html element id.
            static_path (str): output file destination.
    """
    _template = (
    """
    import React from 'react';
    import ReactDOM from 'react-dom';
    import { Router, Route, Link, browserHistory } from 'react-router';

    {% for component, filename in components %}
    import {{component}} from './{{filename}}';
    {% endfor %}

    ReactDOM.render(
      <Router history={ browserHistory }>
      {% for component, route in routes %}
      <Route path='{{route}}' component={ {{component}} } />
      {% endfor %}
      </Router>,
      document.getElementById("{{id}}")
    );

    """)

    def __init__(self, components, element_id, static_path=""):
        routes = get_property(components, "route")
        imports = get_property(components, "filename")

        params = {
            "components": imports,
            "routes": routes,
            "id": element_id
        }

        super(ReactRouter, self).__init__(
            self._template, params, static_path)
        self.to_js()
