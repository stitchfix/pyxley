Core Components
===============

In Pyxley, the core component is the ``UILayout``. This component is
composed of a list of ``charts`` and ``filters``, a single React
component from a JavaScript file, and the Flask app.

::

    # Make a UI
    from pyxley import UILayout
    ui = UILayout(
        "FilterChart",
        "./static/bower_components/pyxley/build/pyxley.js",
        "component_id")


This will create a UI object that's based on the ``FilterChart`` React
component in ``pyxley.js``. It will be bound to an html ``div`` element
called ``component_id``.

If we wanted to add a filter and a chart we could do so with the following

::

    # Make a Button
    cols = [c for c in df.columns if c != "Date"]
    btn = SelectButton("Data", cols, "Data", "Steps")

    # Make a FilterFrame and add the button to the UI
    ui.add_filter(btn)

    # Make a Figure, add some settings, make a line plot
    fig = Figure("/mgchart/", "mychart")
    fig.graphics.transition_on_update(True)
    fig.graphics.animate_on_load()
    fig.layout.set_size(width=450, height=200)
    fig.layout.set_margin(left=40, right=40)
    lc = LineChart(sf, fig, "Date", ["value"], init_params={"Data": "Steps"}, timeseries=True)
    ui.add_chart(lc)


Calling the ``ui.add_chart`` and ``ui.add_filter`` methods simply adds
the components we've created to the layout.

::

    app = Flask(__name__)
    sb = ui.render_layout(app, "./static/layout.js")


Calling ``ui.render_layout`` builds the JavaScript file containing everything we've created.

Charts
------

Charts are meant to span any visualization of data we wish to construct. This includes
line plots, histograms, tables, etc. Several wrappers have been introduced and more
will be added over time.

Implementation
^^^^^^^^^^^^^^

All ``charts`` are ``UIComponents`` that have the following attributes and methods

* An endpoint route method. The user may specify one to override the default.
* A ``url`` attribute that the route function is assigned to by the flask app.
* A ``chart_id`` attribute that specifies the element id.
* A ``to_json`` method that formats the json response.

Filters
-------

Filters are implemented in nearly the same way that ``charts`` are implemented. The only
difference is the lack of the ``to_json`` method.
