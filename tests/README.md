# Pyxley Tests (work-in-progress)

This folder contains an app that can be used for testing purposes. The goal
is to have an element for each component within pyxley. This will serve
as a better testing suite than the examples directory.

## A Different Approach to Pyxley Apps?
The cool thing about this app is that it doesn't require building
any javascript. The pre-built bundle can handle all of pyxley's components.
Before, the main workflow was to write out javascript that was bundled
with npm and wepback. Instead, I've included a bundle that receives
layouts containing props for each of the elements. This pattern is much
more flexible and will allow for easier development.

## How Does It Work?

I've created a react component called `ChartManager` that renders a
list of `PyxleyChart` components by passing two props: `charts` and `filters`.

```javascript
<PyxleyChart
    filters={x.filters}
    charts={x.charts} />
```

where `PyxleyChart` just renders the charts and filters that were passed
in as props. There is a top-level component that fetches the layout
from a flask endpoint. The code can be found in `app/__init__.py`, but
the gist of it is:

```python
@app.route("/api/props/", methods=["GET"])
def props():
    return jsonify({"layouts": _LAYOUTS})

```

`_LAYOUTS` is a list containing the `dict`s that used to be written
out as javascript files. Instead flask, just sends them to the client
and nothing needs to be built.

## What's In Here?

Currently this app will render the following layouts:

1. Filters (from `pyxley.filters`)  
    * `SelectButton`   
    * `ApiButton`  
    * `SliderInput`  
    * `DownloadButton`  

2. Metricsgraphics (from `pyxley.charts.mg`)  
    * `LineChart`  
    * `Histogram`  

More layouts will be added in the future.

## Running

Switch to the `tests` directory and run
```
python app/__init__.py
```
