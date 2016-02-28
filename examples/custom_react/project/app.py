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
from pyxley.charts import Chart
from collections import OrderedDict

from helper import NewChart

parser = argparse.ArgumentParser(description="Flask Template")
parser.add_argument("--env", help="production or local", default="local")
args = parser.parse_args()

TITLE = "Pyxley"

scripts = [
    "./chartfunc.js"
]

css = [
    "./css/main.css"
]

# Make a UI
ui = UILayout(
    "RunLayout",
    "./jsx/custom",
    "component_id")

# Read in the data and stack it, so that we can filter on columns
df = pd.read_csv("./project/static/formatted_run.csv")

# Make a Button
choices = ["Heart Rate", "Pace", "Distance"]
btn = SelectButton("Data", choices, "Data", "Heart Rate")
ui.add_filter(btn)

# Add our new chart
colors = ["#847c77", "#ff5c61"];
nc = NewChart("Seconds", "value", "Altitude", df,
    init_params={"Data": "Heart Rate"}, colors=colors)
ui.add_chart(nc)

app = Flask(__name__)
sb = ui.render_layout(app, "./project/static/layout.js")

# Use the webpack file in the dir and bundle our javascript
from pyxley.utils import Webpack
wp = Webpack(".")
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
