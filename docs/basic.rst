A Basic Pyxley App
==================

Here we will go through building a basic web-application using Pyxley and Flask.

I recommend visiting the `Real Python blog <https://realpython.com/blog/python/the-ultimate-flask-front-end/>`_ for a great intro to a basic app.

::

    App
    |   package.json
    |   .bowerrc
    |   bower.json
    |
    └---project
        |   app.py
        |   templates
        |
        └---static
            |   css
            |   js

Some notes about the above structure

* This assumes that you are running the app from the ``project`` folder.
* Any JavaScript created by the app should go in the ``js`` folder.


JavaScript!
-----------

Node & NPM
^^^^^^^^^^

At the highest level, Node is our biggest JavaScript dependency.
All of the JavaScript dependencies are managed via
`NPM  <https://www.npmjs.com>`_. This document
won't show you how to get Node or NPM, but for Mac OS X users, you can
get it through homebrew.

Note: Prior to version 0.0.9, Bower was used to manage dependencies.
In an effort to simplify the massive amount of dependencies, NPM
will be used as the primary package manager and Bower is completely
optional. In addition, PyReact has been deprecated and will no longer
be used to transpile the jsx code.


HTML & CSS
----------

HTML templates used by flask are stored in the ``templates`` folder. For our purposes,
we only need a really basic template that has a single ``div`` element.

::

     <div id="component_id"></div>

Everything in our app will be tied to this single component.

CSS
^^^

We store any additional CSS we need in the ``static\CSS`` folder.


Flask
-----

Courtesy of the Flask website, "Hello, World!" in Flask looks like the code below.

::

    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    if __name__ == '__main__':
        app.run()

We simply need to build upon this.

Adding Some Pyxley
------------------

Let's start by importing some simple things and building upon the example above. We
will import some ``pyxley`` components, create a UI, and load a data frame.

::

    # Import flask and pandas
    from flask import Flask, render_template
    import pandas as pd

    # Import pyxley stuff
    from pyxley import UILayout
    from pyxley.filters import SelectButton
    from pyxley.charts.mg import LineChart, Figure

    # Read in the data and stack it, so that we can filter on columns
    df = pd.read_csv("fitbit_data.csv")
    sf = df.set_index("Date").stack().reset_index()
    sf = sf.rename(columns={"level_1": "Data", 0: "value"})

    # Make a UI
    ui = UILayout(
        "FilterChart",
        "./static/bower_components/pyxley/build/pyxley.js",
        "component_id")

    # Create the flask app
    app = Flask(__name__)


At this point we now have some data and a layout to build upon. Adding the code
below will add a dropdown select button and a line plot.

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

Now that our ``ui`` object is full of filters and charts, we need
to write out the JavaScript and transpile the jsx code. Previously,
we used PyReact, but unfortunately that has been deprecated. Instead,
we rely on ``webpack``. We have written a wrapper for ``webpack`` that does
the bundling for us.

::
    sb = ui.render_layout(app, "./project/static/layout.js")

    # Create a webpack file and bundle our javascript
    from pyxley.utils import Webpack
    wp = Webpack(".")
    wp.create_webpack_config(
        "layout.js",
        "./project/static/",
        "bundle",
        "./project/static/"
    )
    wp.run()

    @app.route('/', methods=["GET"])
    @app.route('/index', methods=["GET"])
    def index():
        _scripts = ["./bundle.js"]
        css = ["./css/main.css"]
        return render_template('index.html',
            title=TITLE,
            base_scripts=[],
            page_scripts=_scripts,
            css=css)
    if __name__ == '__main__':
        app.run()

``wp.run()`` will transpile "./project/static/layout.js" with the
necessary dependencies and produce "bundle.js". If you had further
dependencies not managed by NPM, you could include them in the
``base_scripts`` keyword argument. 

Now when you run ``app.py`` from the ``project`` folder, accessing your localhost on port 5000 will lead to a simple plot. This example was adapted from the `metricsgraphics example in the <https://github.com/stitchfix/pyxley/blob/master/examples/metricsgraphics/project/app.py>`_ Pyxley repository.
