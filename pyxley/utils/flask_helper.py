import os
from flask import Flask, render_template

DEFAULT_HTML_PARAMS = {
    "page_scripts": ["bundle.js"],
    "base_scripts": [],
    "css": ["main.css"],
    "title": "Pyxley"
}

def create_app(instance_path, static_path, template_path,
    index_params=DEFAULT_HTML_PARAMS, html="index.html"):
    """

        Args:
            instance_path (str): top level
            static_path (str): path to static
    """
    app = Flask(__name__, instance_path=instance_path,
                          instance_relative_config=True,
                          static_folder=static_path,
                          template_folder=template_path)

    def index(name="index"):
        return render_template(html, **index_params)
    app.add_url_rule("/", view_func=index)
    app.add_url_rule("/<string:name>", view_func=index)

    return app

def default_static_path():
    """
        Return the path to the javascript bundle
    """
    fdir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(fdir, '../assets/'))

def default_template_path():
    """
        Return the path to the index.html
    """
    fdir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(fdir, '../assets/'))
