import pkg_resources

from os import environ, path
from flask import Flask, render_template, send_from_directory

import pandas

from buildui import make_ui

here = path.abspath(path.dirname(__file__))

app = Flask(__name__)

ui = make_ui(here+"/fitbit_data.csv")
ui.render_layout(app, "./demo/static/layout.js")

# Create a webpack file and bundle our javascript
from pyxley.utils import Webpack
wp = Webpack(".")
wp.create_webpack_config(
    "layout.js",
    "./demo/static/",
    "bundle",
    "./demo/static/"
)
wp.run()


css = [
    "./css/main.css"
]

@app.route('/', methods=["GET"])
def index():
    _scripts = ["./bundle.js"]
    return render_template('index.html',
        page_scripts=_scripts,
        base_scripts=[],
        css=css,
        title="Plotly Example")

if __name__ == "__main__":
    app.run(debug=True)
