from .react_template import ReactComponent

class UIComponent(object):
    """
    """
    def __init__(self, component_type, options, route_func):
        """"""
        self.params = {
            "type": component_type,
            "options": options
        }
        self.route_func = route_func

    def register_route(self, app):
        """"""
        if "url" not in self.params["options"]:
            raise Exception("Component does not have a URL property")

        if not hasattr(self.route_func, "__call__"):
            raise Exception("No app route function supplied")

        app.add_url_rule(self.params["options"]["url"],
            self.params["options"]["url"],
            self.route_func)
        app.view_functions[self.params["options"]["url"]] = self.route_func

class SimpleComponent(object):
    def __init__(self, layout, src_file, component_id, props):
        self.layout = layout
        self.src_file = src_file
        self.component_id = component_id
        self.props = props

    def render(self, path):
        return ReactComponent(
            self.layout,
            self.src_file,
            self.component_id,
            props=self.props,
            static_path=path)

class UILayout(object):

    def __init__(self, layout, src_file, component_id, dynamic=True, filter_style="'btn-group'"):
        self.layout = layout
        self.src_file = src_file
        self.component_id = component_id
        self.filter_style = filter_style
        self.filters = []
        self.charts = []
        self.dynamic = dynamic

    def add_filter(self, component):
        if getattr(component, "name") != "Filter":
            raise Exception("Component is not an instance of Filter")
        self.filters.append(component)

    def add_chart(self, component):
        if getattr(component, "name") != "Chart":
            raise Exception("Component is not an instance of Chart")
        self.charts.append(component)

    def build_props(self):
        props = {}
        if self.filters:
            props["filters"] = [f.params for f in self.filters]
        if self.charts:
            props["charts"] = [c.params for c in self.charts]

        props["dynamic"] = self.dynamic
        props["filter_style"] = self.filter_style
        return props

    def assign_routes(self, app):
        for f in self.filters:
            if f.route_func:
                f.register_route(app)

        for c in self.charts:
            if c.route_func:
                c.register_route(app)

    def render_layout(self, app, path):
        self.assign_routes(app)
        return ReactComponent(
            self.layout,
            self.src_file,
            self.component_id,
            props=self.build_props(),
            static_path=path)
