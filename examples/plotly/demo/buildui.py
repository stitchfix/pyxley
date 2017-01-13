from pyxley.charts.plotly import PlotlyAPI
from pyxley.filters import SelectButton
from pyxley import UILayout, register_layouts
import pandas as pd

from flask import jsonify, request

def make_ui(filename):
    df = pd.read_csv(filename)

    # Make a UI
    ui = UILayout("FilterChart", "component_id")

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


def get_layouts(mod, filename):

    # plotly
    plotly_ui = make_ui(filename)
    plotly_ui.assign_routes(mod)
    plotly_props = plotly_ui.build_props()

    _layouts = {
        "plotly": {
            "layout": [plotly_props],
            "title": "Plotly"
        }
    }

    register_layouts(_layouts, mod)
