from flask import Flask
from flask import request, jsonify, render_template, make_response
import pandas as pd
import json
import sys
import glob
import numpy as np
import argparse

from pyxley import UILayout
from pyxley.filters import SelectButton
from pyxley.charts.mg import LineChart, Figure, ScatterPlot, Histogram
from pyxley.charts.datatables import DataTable
from collections import OrderedDict

parser = argparse.ArgumentParser(description="Flask Template")
parser.add_argument("--env", help="production or local", default="local")
args = parser.parse_args()

TITLE = "Pyxley"

scripts = []

css = ["./css/main.css"]

# Make a UI
ui = UILayout(
    "FilterChart",
    "pyxley",
    "component_id",
    filter_style="''")

# Read in the data and stack it, so that we can filter on columns
df = pd.read_csv("project/fitbit_data.csv")
sf = df.set_index("Date").stack().reset_index()
sf = sf.rename(columns={"level_1": "Data", 0: "value"})

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

# Now make a FilterFrame for the histogram
hFig = Figure("/mghist/", "myhist")
hFig.layout.set_size(width=450, height=200)
hFig.layout.set_margin(left=40, right=40)
hFig.graphics.animate_on_load()
# Make a histogram with 20 bins
hc = Histogram(sf, hFig, "value", 20, init_params={"Data": "Steps"})
ui.add_chart(hc)

# Let's play with our input
df["Date"] = pd.to_datetime(df["Date"])
df["week"] = df["Date"].apply(lambda x: x.isocalendar()[1])
gf = df.groupby("week").agg({
        "Date": [np.min, np.max],
        "Steps": np.sum,
        "Calories Burned": np.sum,
        "Distance": np.sum
    }).reset_index()
f = lambda x: '_'.join(x) if (len(x[1]) > 0) and x[1] != 'sum' else x[0]
gf.columns = [f(c) for c in gf.columns]
gf = gf.sort_index(by="week", ascending=False)
gf["Date_amin"] = gf["Date_amin"].apply(lambda x: x.strftime("%Y-%m-%d"))
gf["Date_amax"] = gf["Date_amax"].apply(lambda x: x.strftime("%Y-%m-%d"))

cols = OrderedDict([
    ("week", {"label": "Week"}),
    ("Date_amin", {"label": "Start Date"}),
    ("Date_amax", {"label": "End Date"}),
    ("Calories Burned", {"label": "Calories Burned"}),
    ("Steps", {"label": "Steps"}),
    ("Distance", {"label": "Distance (mi)", "format": "%5.2f"})
])

tb = DataTable("mytable", "/mytable/", gf, columns=cols, paging=True, pageLength=5)
ui.add_chart(tb)

app = Flask(__name__)
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
    return render_template('index.html',
        title=TITLE,
        base_scripts=scripts,
        page_scripts=_scripts,
        css=css)

if __name__ == "__main__":
    app.run(debug=True)
