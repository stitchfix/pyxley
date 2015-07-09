from flask import Flask
from flask import request, jsonify, render_template, make_response
import pandas as pd
import json
import sys
import glob
import numpy as np
import argparse

from pyxley import UILayout
from pyxley.filters import SelectButton, SliderInput
from pyxley.charts.datamaps import DatamapUSA


parser = argparse.ArgumentParser(description="Flask Template")
parser.add_argument("--env", help="production or local", default="local")
args = parser.parse_args()

TITLE = "Pyxley"

scripts = [
    "./bower_components/jquery/dist/jquery.min.js",
    "./bower_components/d3/d3.min.js",
    "./bower_components/topojson/topojson.js",
    "./bower_components/datamaps/dist/datamaps.usa.min.js",
    "./bower_components/require/build/require.min.js",
    "./bower_components/react/react.js",
    "./bower_components/react-bootstrap/react-bootstrap.min.js",
    "./bower_components/pyxley/build/pyxley.js",
]

css = [
    "./bower_components/bootstrap/dist/css/bootstrap.min.css",
    "./css/main.css"
]

# Make a UI
ui = UILayout(
    "FilterChart",
    "./static/bower_components/pyxley/build/pyxley.js",
    "component_id",
    filter_style="''")


df = pd.read_csv("./static/Colorful_State.csv")
df.month = df.month.astype('str')

sldr = SliderInput("Month", 1, 13, "month", "1")
ui.add_filter(sldr)

dm = DatamapUSA("/data_map/", "mapid", df,  "state", "color1", init_params={"month": "1"})
ui.add_chart(dm)

app = Flask(__name__)
sb = ui.render_layout(app, "./static/layout.js")


@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def index():
    _scripts = ["./layout.js"]
    return render_template('index.html',
        title=TITLE,
        base_scripts=scripts,
        page_scripts=_scripts,
        css=css)

if __name__ == "__main__":
    app.run(debug=True)