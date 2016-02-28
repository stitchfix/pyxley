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

TITLE = "Pyxley"

scripts = []

css = [
    "./css/main.css"
]

# Make a UI
ui = UILayout(
    "FilterChart",
    "pyxley",
    "component_id",
    filter_style="''")


df = pd.read_csv("./project/static/Colorful_State.csv")
df.month = df.month.astype('str')

sldr = SliderInput("Month", 1, 13, "month", "1")
ui.add_filter(sldr)

dm = DatamapUSA("/data_map/", "mapid", df,  "state", "color1", init_params={"month": "1"})
ui.add_chart(dm)

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
