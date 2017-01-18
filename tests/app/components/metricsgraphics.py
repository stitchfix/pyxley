from pyxley.charts.mg import Figure, Histogram, LineChart, ScatterPlot
from pyxley.filters import SelectButton
from pyxley import UILayout
import pandas as pd

from flask import request, jsonify

def create_line_plot(df):
    """ create a mg line plot

        Args:
            df (pandas.DataFrame): data to plot
    """
    fig = Figure("/mg/line_plot/", "mg_line_plot")
    fig.graphics.transition_on_update(True)
    fig.graphics.animate_on_load()
    fig.layout.set_size(width=450, height=200)
    fig.layout.set_margin(left=40, right=40)
    return LineChart(df, fig, "Date", ["value"],
        init_params={"Data": "Steps"}, timeseries=True)

def create_histogram(df):
    """ create a mg line plot

        Args:
            df (pandas.DataFrame): data to plot
    """
    fig = Figure("/mg/histogram/", "mg_histogram")
    fig.layout.set_size(width=450, height=200)
    fig.layout.set_margin(left=40, right=40)
    fig.graphics.animate_on_load()

    # Make a histogram with 20 bins
    return Histogram(df, fig, "value", 20, init_params={"Data": "Steps"})

def create_scatterplot(df):
    """ create a mg line plot

        Args:
            df (pandas.DataFrame): data to plot
    """
    fig = Figure("/mg/scatter/", "mg_scatter")
    fig.layout.set_size(width=450, height=200)
    fig.layout.set_margin(left=40, right=40)
    fig.graphics.animate_on_load()

    init_params = {"Data": "Steps"}

    def get_data():
        y = request.args.get("Data", "Steps")
        return jsonify(ScatterPlot.to_json(df, "Steps", y))

    # Make a histogram with 20 bins
    return ScatterPlot(df, fig, "Steps", "Distance",
        init_params={}, route_func=get_data)

def make_mg_layout():
    # load a dataframe
    filename = "../examples/metricsgraphics/project/fitbit_data.csv"
    df = pd.read_csv(filename)

    # Make a UI
    ui = UILayout(
        "FilterChart",
        "component_id")

    # Make a Button
    cols = [c for c in df.columns if c != "Date"]
    btn = SelectButton("Data", cols, "Data", "Steps")

    # add the button to the UI
    ui.add_filter(btn)

    # stack the dataframe
    _stack = df.set_index("Date").stack().reset_index()
    _stack = _stack.rename(columns={"level_1": "Data", 0: "value"})

    # Make a Figure, add some settings, make a line plot
    ui.add_chart(create_line_plot(_stack))
    ui.add_chart(create_histogram(_stack))
    ui.add_chart(create_scatterplot(df))

    return ui
