Pyxley In Production
====================

Now that we've built an app, how do we deploy it? Because Pyxley
is built on top of Flask, the process for deploying our app
is no different than deploying any other Flask app. Rather than
cover the basics of deploying web apps, this guide will cover
some patterns and address some of Pyxley's capabilities.

Data and DataFrames
-------------------
Pyxley was developed specifically with Pandas in mind. Each
widget has methods for transforming dataframes into JSON
objects that the different JavaScript libraries can interpret.
It's not entirely obvious how to deal with issues such as
reloading data.

Updating Data
^^^^^^^^^^^^^
Let's revisit our MetricsGraphics example, specifically the
``LineChart`` object. Recall when we created the object,
we passed it a dataframe and it looked something like
the snippet below.

::
    # sf is our dataframe
    # fig is our figure object
    lc = LineChart(sf, fig, "Date", ["value"], **kwargs)

When the dataframe, ``sf``, is passed into the constructor
it is passed into a function that Flask will use any time
it needs the chart data.

In the ``__init__`` method you will find the following
snippet.

::
    if not route_func:
        def get_data():
            args = {}
            for c in init_params:
                if request.args.get(c):
                    args[c] = request.args[c]
                else:
                    args[c] = init_params[c]
            return jsonify(LineChart.to_json(
                    self.apply_filters(df, args),
                    x,
                    y,
                    timeseries=timeseries
                ))
        route_func = get_data

The default behavior for ``LineChart`` is to use this
basic route function. Let's focus on the data that
gets returned for a moment. Notice we call ``jsonify``
which is a Flask function that turns a python ``dict``
into a JSON object. The input ``dict`` is returned
by the ``LineChart.to_json`` method. ``to_json`` takes
a dataframe as the input as well as a few other variables.
``self.apply_filters`` is a method belonging to the ``Chart``
base class that takes a dataframe and a ``dict`` containing
our filtering conditions.

As far as default behavior, this is perfectly reasonable, but
it makes a pretty rigid assumption that the underlying data
will not change. This default route function is created when
the ``LineChart`` object is initialized and changing the data
would require us to recreate the object. In practice, it's not
a good idea to have a dependency that requires an app to be
restarted.

Now notice the first line of our snippet: ``if not route_func``.
``route_func`` is a keyword argument in the ``__init__`` method.
If a developer provides their own route function, they are no
longer restricted by the default behavior.

Reloading Dataframes
^^^^^^^^^^^^^^^^^^^^
Let's assume that we are perfectly comfortable with using
Pandas as our data source, but we would like to be able to
refresh the data on some cadence.

Returning to our ``LineChart`` example, what if created
it in the following way:

::
    # sf is our dataframe
    # fig is our figure object
    lc = LineChart(sf, fig, "Date", ["value"],
        route_func=some_other_route,
        **kwargs)

Now that we have passed in ``some_other_route`` it will
be used instead and ``sf`` will be ignored. So let's
start building what the function looks like.

::
    class MyDataWrapper(object):
        """ We are building a simple wrapper for our data
        """
        def __init__(df, x, y, timeseries=True):
            self.df = df
            self.x = x
            self.y = y
            self.timeseries = timeseries

        def my_route_function(self):
            # put args check here
            return jsonify(LineChart.to_json(
                    Chart.apply_filters(self.df, args),
                    self.x,
                    self.y,
                    timeseries=self.timeseries
                ))

So the first thing you should notice is that this
looks pretty similar to our default ``get_data`` function
from above. The most obvious difference is that now
most of the variables are now member variables of our
``MyDataWrapper`` class. The main benefit from this is
that now we are calling a method in our ``MyDataWrapper``
object that also manages the state of our dataframe
``self.df``. Now that ``LineChart`` no longer has anything
to do with our dataframe and how to parse it, we are free to
reload our data. You could imagine adding a ``set_data``
method to our class that has logic about how and when to
reload data. The snippet below shows how to modify our example.
We will still pass in all of the necessary chart options,
but the important logic is now handled by our new object.

::
    # sf is our dataframe
    myData = MyDataWrapper(sf, "Date", ["value"])
    # fig is our figure object
    lc = LineChart(sf, fig, "Date", ["value"],
        route_func=myData.my_route_function,
        **kwargs)

Databases
^^^^^^^^^
What if your data is too big. Say, for example, you would
like to use ``guincorn`` and the idea of replicating your
data across multiple processes just isn't feasible. If you
are using a relational database that works with ``SQLAlchemy``
there's not much to change. The snippet below shows one
possible change to our data wrapper from above. It's also
important to remember that we just need to format our data
for the JavaScript libraries. We can freely customize the
methods to accommodate any data source.

::
    class MyDataWrapper(object):
        """ We are building a simple wrapper for our data
        """
        def __init__(sql_engine, x, y, timeseries=True):

            self.engine = sql_engine
            self.x = x
            self.y = y
            self.timeseries = timeseries

        def get_data(self, args):
            # make some sql query or use SQLAlchemy functions
            return pd.read_sql('select * from table', self.engine)

        def my_route_function(self):
            # put args check here
            df = get_data(args)
            return jsonify(LineChart.to_json(
                    Chart.apply_filters(df, args),
                    self.x,
                    self.y,
                    timeseries=self.timeseries
                ))



REST APIs
^^^^^^^^^
What if you want to hit some other API? Use ``requests``! Then
it's the same game of just leveraging the other functions to
get the data in the format the chart needs. 
