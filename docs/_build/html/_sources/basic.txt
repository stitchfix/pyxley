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

At the highest level, Node is our biggest JavaScript dependency. PyReact
needs a JavaScript runtime and Node fills that role. In addition, we
can use `NPM <https://www.npmjs.com>`_ to install Bower. This document
won't show you how to get Node or NPM, but for Mac OS X users, you can
get it through homebrew.

Once you have NPM, simply type

::

    npm install -g bower

This will give bower global access so that you can execute it.

Bower
^^^^^

`Bower <http://bower.io/>`_ is a great package manager. In the examples
directory, each of the examples has a ``bower.json`` file. This file
contains all the necessary packages for the app to run. Install the
packages by typing ``bower install`` in the directory of the ``bower.json``
file. There is a file called ``.bowerrc`` that specifies the location that
bower will store the libraries.


If the ``.bowerrc`` file looks like

::

    {
        "directory": "./project/static/bower_components"
    }

Then the folder structure in static should look like the figure below after installation.

::

    └---static
        |   css
        |   js
        |   bower_components


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

Finally, we need to transform all of the inputs into javascript and render the HTML template.
This assumes that the ``index.html`` template has all of the javascript and css files specified
in the HTML.

::

    sb = ui.render_layout(app, "./static/layout.js")

    @app.route('/', methods=["GET"])
    def index():
        return render_template('index.html')

    if __name__ == '__main__':
        app.run()

Now when you run ``app.py`` from the ``project`` folder, accessing your localhost on port 5000 will lead to a simple plot. This example was adapted from the `metricsgraphics example in the <https://github.com/stitchfix/pyxley/blob/master/examples/metricsgraphics/project/app.py>`_ Pyxley repository.


