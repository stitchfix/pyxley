# Pyxley

The Pyxley python library makes use of the [pyxleyJS](https://github.com/stitchfix/pyxleyJS) React components to create Flask-based web applications. Through the use of the PyReact library, we can use Jinja templating to construct and transform a single React component. The specific UI components are passed as props to the parent component. A simpler interface is provided through the use of specific wrappers for each of the component types.

<img src="http://multithreaded.stitchfix.com/assets/images/blog/pyxley_examples_grid.png">

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

## Documentation and Testing
### Documentation
Available at [readthedocs](http://pyxley.readthedocs.org/)

### Testing
Coming Soon!

## Python versions
Currently supporting Python 2 and 3.

## Installation
Install via pip
```
pip install pyxley
```

## metricsgraphics.js Example
An example flask app has been included. It demonstrates how to add a filter and several charts.


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



