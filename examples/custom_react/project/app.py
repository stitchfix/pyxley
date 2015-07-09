from flask import Flask
from flask import request, jsonify, render_template, make_response
import pandas as pd
import json
import sys
import glob
import numpy as np
import argparse

from react import jsx

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
    "./bower_components/jquery/dist/jquery.min.js",
    "./bower_components/d3/d3.min.js",
    "./bower_components/nvd3/build/nv.d3.js",
    "./chartfunc.js",
    "./bower_components/require/build/require.min.js",
    "./bower_components/react/react.js",
    "./bower_components/react-bootstrap/react-bootstrap.min.js",
    "./bower_components/pyxley/build/pyxley.js",
]

css = [
    "./bower_components/bootstrap/dist/css/bootstrap.min.css",
    "./bower_components/nvd3/build/nv.d3.min.css",
    "./css/main.css"
]

transformer = jsx.JSXTransformer()
jsx_input = "static/jsx/"
jsx_output = "static/js/"

for f in glob.glob(jsx_input+"*.js"):
    transformer.transform(f,js_path=jsx_output+f.split('/')[-1])

# Make a UI
ui = UILayout(
    "RunLayout",
    "./static/js/custom.js",
    "component_id")

# Read in the data and stack it, so that we can filter on columns
df = pd.read_csv("./static/formatted_run.csv")

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
sb = ui.render_layout(app, "./static/layout.js")


@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def index():
    _scripts = ["./layout.js", "./js/navbar.js"]
    return render_template('index.html',
        title=TITLE,
        base_scripts=scripts,
        page_scripts=_scripts,
        css=css)

if __name__ == "__main__":
    app.run(debug=True)