from flask import Flask
from flask import request, jsonify, render_template, make_response
import pandas as pd
import json
import sys
import glob
from react import jsx

import numpy as np
import re
import argparse

from pyxley.charts.datatables import DataTable
from pyxley import SimpleComponent
from pyxley.filters import SelectButton

from collections import OrderedDict
parser = argparse.ArgumentParser(description="Flask Template")
parser.add_argument("--env", help="production or local", default="local")
args = parser.parse_args()

TITLE = "Pyxley"

scripts = [
    "./conf_int.js"
    ]

css = [
    "./css/main.css"
]

df = pd.DataFrame(json.load(open("./project/static/data.json", "r")))
df = df.dropna()
df["salary"] = df["salary"].apply(lambda x: float(re.sub("[^\d\.]", "", x)))
df["lower"] = ( 1. - (0.03*np.random.randn(df.shape[0]) + 0.15))
df["upper"] = ( 1. + (0.03*np.random.randn(df.shape[0]) + 0.15))
df["salary_upper"] = df["upper"]*df["salary"]
df["salary_lower"] = df["lower"]*df["salary"]

cols = OrderedDict([
    ("position", {"label": "Position"}),
    ("office", {"label": "Office"}),
    ("start_date", {"label": "Start Date"}),
    ("salary_lower", {"label": "Salary Range",
        "confidence": {
            "lower": "salary_lower",
            "upper": "salary_upper"
        }
    })
])

addfunc = """

new $.fn.dataTable.FixedColumns(this, {
    leftColumns: 1,
    rightColumns: 0
});
confidence_interval(this.api().column(3, {"page":"current"}).data(), "mytable");
"""

drawfunc = """
confidence_interval(this.api().column(3, {"page":"current"}).data(), "mytable");
"""


tb = DataTable("mytable", "/mytable/", df,
    columns=cols,
    paging=True,
    pageLength=9,
    scrollX=True,
    columnDefs=[{
        "render": """<svg width="156" height="20"><g></g></svg>""",
        "orderable": False,
        "targets": 3
    }],
    sDom='<"top">rt<"bottom"lp><"clear">',
    deferRender=True,
    initComplete=addfunc,
    drawCallback=drawfunc)


app = Flask(__name__)
tb.register_route(app)


ui = SimpleComponent(
    "Table",
    "pyxley",
    "component_id",
    tb.params
)

sb = ui.render("./project/static/layout.js")

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

@app.route('/test', methods=["GET"])
def testtest():
    return jsonify(jsfunc)

@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def index():
    _scripts = [
        "./bundle.js", "./dataTables.fixedColumns.js"
        ]
    return render_template('index.html',
        title=TITLE,
        base_scripts=scripts,
        page_scripts=_scripts,
        css=css)

if __name__ == "__main__":
    app.run(debug=True)
