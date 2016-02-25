from .react_template import ReactComponent

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
            dynamic (bool): whether or not to have dynamic buttons
            filter_style (str): css for filters

    """
    def __init__(self, layout, src_file, component_id, dynamic=True,
        filter_style="'btn-group'"):
        
        self.layout = layout
        self.src_file = src_file
        self.component_id = component_id
        self.filter_style = filter_style
        self.filters = []
        self.charts = []
        self.dynamic = dynamic

    def add_filter(self, component):
        """Add a filter to the layout."""
        if getattr(component, "name") != "Filter":
            raise Exception("Component is not an instance of Filter")
        self.filters.append(component)

    def add_chart(self, component):
        """Add a chart to the layout."""
        if getattr(component, "name") != "Chart":
            raise Exception("Component is not an instance of Chart")
        self.charts.append(component)

    def build_props(self):
        """Build the props dictionary."""
        props = {}
        if self.filters:
            props["filters"] = [f.params for f in self.filters]
        if self.charts:
            props["charts"] = [c.params for c in self.charts]

        props["dynamic"] = self.dynamic
        props["filter_style"] = self.filter_style
        return props

    def assign_routes(self, app):
        """Register routes with the app."""
        for f in self.filters:
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
