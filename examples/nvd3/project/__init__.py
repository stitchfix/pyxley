from os import path
from buildui import get_layouts

from pyxley.utils import create_app, default_static_path, default_template_path
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
check_for_bundle(path_to_static)

app = create_app(here, path_to_static, default_template_path())

# build the layout
get_layouts(app, here+"/static/formatted_run.csv")

if __name__ == "__main__":
    app.run(debug=True)
