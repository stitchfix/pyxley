from os import path
from buildui import get_layouts
from flask import Flask, render_template
from pyxley.utils import default_static_path, create_app

import shutil
def check_for_bundle(path_to_static):
    # check if bundle.js exists
    if not path.isfile(path_to_static+"/bundle.js"):
        # grab the bundle
        _path_to_bundle = default_static_path() + "/bundle.js"
        shutil.copy2(_path_to_bundle, path_to_static)

# create the flask app
here = path.abspath(path.dirname(__file__))
path_to_static = here + "/static"

# check for the bundle
check_for_bundle(path_to_static)

# create html parameters
html_params = {
    "page_scripts": ["./bundle.js" ],
    "base_scripts": ["./conf_int.js"],
    "title": "DataTables",
    "css": ["./css/main.css"]
}

# Create the flask app
app = create_app(here, path_to_static, here+"/templates",
    index_params=html_params)

# build the layout
get_layouts(app, "./project/static/data.json")

if __name__ == "__main__":
    app.run(debug=True)
