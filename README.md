# Pyxley

The Pyxley python library makes use of the Pyxley.js React components to create Flask-based web applications. Through the use of the PyReact library, we can use Jinja templating to construct and transform a single React component. The specific UI components are passed as props to the parent component. A simpler interface is provide through the use of specific wrappers for each of the component types.

An example of the Jinja template for a single React component is presented below.
```python
    _react = (
    """
    var Component = require("{{path}}").{{name}};
    {{vars}}
    React.render(
        <Component
        {{props}} />,
        document.getElementById("{{id}}")
    );
    """)
```

By constructing the template in this way, the developer can easily integrate a custom React component. The only requirements are the props, elementId, and location of the React component.

## UIComponent
The React components in Pixley.js were designed to retrieve data from an API. For this library, we have chosen Flask. As such, Flask specific classes have been written to simplify the creation of components. Each component must have a type, options, and a route from which the data will be retrieved. The base class for these components is presented below. Each component packages the parameters in a dict and has the ability to register an url with the Flask app.

```python
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
```

## Filters & Charts
Each Filter and Chart inherits from the base UIComponent class. Wrappers have been written to provide a clearer interface. An example of a “SelectButton” is provided below. The user only specifies the options, while the type is set by the implementation.

```python
class SelectButton(Filter):
    """
    """
    def __init__(self, label, items, filter_id, default):
        opts = {
            "label": label,
            "items": items,
            "alias": filter_id,
            "default": default
        }
        super(SelectButton, self).__init__("SelectButton", opts, None)
```

## UILayout
The UILayout class is designed to integrate the filters and charts with the Flask app. It collects the UIComponents and registers the relevant urls with the app. Within this class, the developer must specify the React layout component, the location of the source jsx file, and the elementid for which the component will be mounted.

## Pandas Integration
This library is built with the pandas dataframe in mind. That is, we expect the data to be some sort of structured data that’s easy to filter and easy to plot. Each Javascript charting library has it’s own expected format for the data which makes integration with python challenging. Included in this library are several helper functions that format the data in the way the Javascript libraries are expecting.


