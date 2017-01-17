from os import path
from buildui import get_layouts
from flask import Flask, render_template
from pyxley.utils import default_static_path

import shutil
def check_for_bundle(path_to_static):
    # check if bundle.js exists
    if not path.isfile(path_to_static+"/bundle.js"):
        # grab the bundle
        _path_to_bundle = default_static_path() + "/bundle.js"
        shutil.copy2(_path_to_bundle, path_to_static)

# create the flask app
here = path.abspath(path.dirname(__file__))
path_to_static = here + "/static/"

# check for the bundle
check_for_bundle(path_to_static)

# Create the flask app 
app = Flask(__name__)

# build the layout
get_layouts(app, "./project/static/data.json")

@app.route('/', methods=["GET"])
@app.route('/<string:name>', methods=["GET"])
def index(name="index"):
    _scripts = [
        "./bundle.js", "./dataTables.fixedColumns.js"
        ]
    return render_template('index.html',
        title="DataTables",
        base_scripts=["./conf_int.js"],
        page_scripts=_scripts,
        css=["./css/main.css"])

if __name__ == "__main__":
    app.run(debug=True)
