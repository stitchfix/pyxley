import pandas as pd
import numpy as np
from pyxley.charts.nvd3 import TwoAxisFocus, PieChart
from pyxley.filters import SelectButton
from pyxley import UILayout, register_layouts

def two_axis_focus(df):
    init_params = {"Data": "Heart Rate"}
    colors = ["#847c77", "#ff5c61"]
    _chart = TwoAxisFocus("Seconds", "value", "Altitude", df,
        chart_id="nvd3_focus", url="/api/nvd3_focus/",
        init_params=init_params, colors=colors)
    return _chart

def pie_chart(df):
    _hr = df.loc[df["Data"] == "Heart Rate"].copy()

    def bucket_hr(x):
        if x < 110:
            return "Resting"
        if x < 135:
            return "Fat Burn"
        if x < 153:
            return "Cardio"
        return "Peak"
    _hr = _hr.assign(hr_zone=_hr["value"].apply(bucket_hr))

    # group by and aggregate
    grp_hr = _hr.groupby("hr_zone").size().reset_index()
    grp_hr.columns = ["hr_zone", "fraction"]
    grp_hr["fraction"] = grp_hr["fraction"].astype("float")

    # pivot
    _pivot = pd.pivot_table(grp_hr, values=["fraction"],
        columns=["hr_zone"], fill_value=0, aggfunc=np.max).reset_index()
    colors = ["#7bc9c1", "#7f7f7f", "#1f77b4", "#393b79"]
    values = {k:k for k in grp_hr.hr_zone.unique()}

    pc = PieChart(values, _pivot, colors=colors)
    return pc

def make_nv_layout():
    # load the data
    filename = "../examples/nvd3/project/static/formatted_run.csv"
    df = pd.read_csv(filename)

    ui = UILayout("FilterChart")

    # Make a button
    choices = ["Heart Rate", "Pace", "Distance"]
    btn = SelectButton("Data", choices, "Data", "Heart Rate")
    ui.add_filter(btn)

    # Add the chart
    ui.add_chart(two_axis_focus(df))
    ui.add_chart(pie_chart(df))
    return ui
