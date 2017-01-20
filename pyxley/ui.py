from .react_template import ReactComponent
from collections import OrderedDict
from flask import jsonify

def register_layouts(layouts, app, url="/api/props/", brand="Pyxley"):
    """ register UILayout with the flask app

        create a function that will send props for each UILayout

        Args:
            layouts (dict): dict of UILayout objects by name
            app (object): flask app
            url (string): address of props; default is /api/props/
    """
    def props(name):
        if name not in layouts:
            # cast as list for python3
            name = list(layouts.keys())[0]
        return jsonify({"layouts": layouts[name]["layout"]})

    def apps():
        paths = []
        for i, k in enumerate(layouts.keys()):
            if i == 0:
                paths.append({
                    "path": "/",
                    "label": layouts[k].get("title", k)
                })

            paths.append({
                "path": "/"+k,
                "label": layouts[k].get("title", k)
            })

        return jsonify({"brand": brand, "navlinks": paths})

    app.add_url_rule(url+"<string:name>/", view_func=props)
    app.add_url_rule(url, view_func=apps)

class UIComponent(object):
    """Base React UI component.

        Every UI component is derived from this component. Both
        charts and filters inherit these methods. This class allows
        the chart to register the endpoint with the flask application.

        Args:
            component_type (str): Type of component to build.
            options (dict): options specific to the component type.
            route_func (function): endpoint function.

    """
    def __init__(self, component_type, options, route_func):
        """"""
        self.params = {
            "type": component_type,
            "options": options
        }
        self.route_func = route_func

    def register_route(self, app):
        """Register the api route function with the app."""
        if "url" not in self.params["options"]:
            raise Exception("Component does not have a URL property")

        if not hasattr(self.route_func, "__call__"):
            raise Exception("No app route function supplied")

        app.add_url_rule(self.params["options"]["url"],
            self.params["options"]["url"],
            self.route_func)


class SimpleComponent(object):
    """Simple class for rendering a single component.

        Rather than requiring a collection of filters and charts, this
        function will render a single react component with props
        passed as a dictionary.

        Args:
            layout (str): Type of react component to create.
            src_file (str): javascript file containing the component.
            component_id (str): html element id.
            props (dict): props for the component.
    """
    def __init__(self, layout, src_file, component_id, props):
        self.layout = layout
        self.src_file = src_file
        self.component_id = component_id
        self.props = props

    def render(self, path):
        """Render the component to a javascript file."""
        return ReactComponent(
            self.layout,
            self.src_file,
            self.component_id,
            props=self.props,
            static_path=path)

class UILayout(object):
    """Simple UI layout.

        This class handles the construction of a single javascript file
        based on the inputs provided. It aggregates the properties specified
        over the different charts and filters and creates a single set of
        props.

        This relies on the creation of a single React component that is comprised
        of charts and filters. An example can be found at
        https://github.com/stitchfix/pyxleyJS/blob/master/src/layouts.js

        Args:
            layout (str): name of react component to render.
            src_file (str): location of javascript containing the component.
            component_id (str): html element id.

    """
    def __init__(self, layout, component_id="component_id", src_file='pyxley'):

        self.layout = layout
        self.src_file = src_file
        self.component_id = component_id
        self.filters = OrderedDict()
        self.charts = []

    def add_filter(self, component, filter_group="pyxley-filter"):
        """Add a filter to the layout."""
        if getattr(component, "name") != "Filter":
            raise Exception("Component is not an instance of Filter")
        if filter_group not in self.filters:
            self.filters[filter_group] = []
        self.filters[filter_group].append(component)

    def add_chart(self, component):
        """Add a chart to the layout."""
        if getattr(component, "name") != "Chart":
            raise Exception("Component is not an instance of Chart")
        self.charts.append(component)

    def build_props(self):
        """Build the props dictionary."""
        props = {}
        if self.filters:
            props["filters"] = {}
            for grp in self.filters:
                props["filters"][grp] = [f.params for f in self.filters[grp]]
        if self.charts:
            props["charts"] = [c.params for c in self.charts]

        props["type"] = self.layout
        return props

    def assign_routes(self, app):
        """Register routes with the app."""
        for grp in self.filters:
            for f in self.filters[grp]:
                if f.route_func:
                    f.register_route(app)

        for c in self.charts:
            if c.route_func:
                c.register_route(app)

    def render_layout(self, app, path, alias=None):
        """Write to javascript."""
        self.assign_routes(app)
        return ReactComponent(
            self.layout,
            self.src_file,
            self.component_id,
            props=self.build_props(),
            static_path=path,
            alias=alias)
