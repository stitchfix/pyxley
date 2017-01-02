import pkg_resources

from os import environ, path
from flask import Flask, render_template, send_from_directory
from flask import jsonify
import pandas

from build_ui import get_layouts

here = path.abspath(path.dirname(__file__))


app = Flask(__name__)

# add the blueprint
from components.helpers import get_mod
_mod = get_mod()
_LAYOUTS = get_layouts(_mod)

app.register_blueprint(_mod)


@app.route("/api/props/", methods=["GET"])
def props():
    return jsonify({
        "layouts": _LAYOUTS
        })

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html',
        page_scripts=["./bundle.js"],
        base_scripts=[],
        css=["./css/main.css"],
        title="Plotly Example")

if __name__ == "__main__":
    app.run(debug=True)
