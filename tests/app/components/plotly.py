
from pyxley.charts.plotly import PlotlyAPI
from pyxley.filters import SelectButton
from pyxley import UILayout
import pandas as pd

from flask import jsonify, request

def make_plotly_ui():
    filename = "../examples/metricsgraphics/project/fitbit_data.csv"
    df = pd.read_csv(filename)

    # Make a UI
    ui = UILayout(
        "PyxleyChart",
        "component_id")

    # Read in the data and stack it, so that we can filter on columns
    _stack = df.set_index("Date").stack().reset_index()
    _stack = _stack.rename(columns={"level_1": "Data", 0: "value"})

    # Make a Button
    cols = [c for c in df.columns if c != "Date"]
    btn = SelectButton("Data", cols, "Data", "Steps")

    # add the button to the UI
    ui.add_filter(btn)

    init_params = {"Data": "Steps"}
    def get_data():
        args = {}
        for c in init_params:
            if request.args.get(c):
                args[c] = request.args[c]
            else:
                args[c] = init_params[c]
        return jsonify(
            PlotlyAPI.line_plot(
                PlotlyAPI.apply_filters(_stack, args),
                [("Date", "value")],
                "lines+markers",
                {}
            ))
    _plot = PlotlyAPI(
        "plotly_chart",
        "/api/plotly_line_plot/",
        get_data,
        init_params=init_params
    )
    ui.add_chart(_plot)
    return ui
