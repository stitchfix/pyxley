import pkg_resources

from os import environ, path
from pyxley.utils import create_app
from flask import jsonify
import pandas

from build_ui import get_layouts

here = path.abspath(path.dirname(__file__))
path_to_static = here + "/static"
path_to_tempates = here + "/templates"
html_params = {
    "page_scripts": ["./bundle.js"],
    "base_scripts": ["./conf_int.js"],
    "css": ["./css/main.css"],
    "title": "Pyxley Tests"
}
app = create_app(here, path_to_static, path_to_tempates,
    index_params=html_params)

# add the blueprint
from components.helpers import get_mod
_mod = get_mod()
get_layouts(_mod)

app.register_blueprint(_mod)

if __name__ == "__main__":
    app.run(debug=True)
