from __future__ import print_function

import os
import sys
import json

from ..react_template import ReactTemplate
from subprocess import check_call

def run(cmd, *args, **kwargs):
    """"""
    kwargs["shell"] = (sys.platform == "win32")
    return check_call(cmd, *args, **kwargs)

class NPM(object):
    package_template = ("""
    {
      "name": "{{name}}",
      "version": "{{version}}",
      "description": "",
      "main": "{{main}}",
      "scripts": {{scripts}},
      "author": "",
      "license": "MIT",
      "devDependencies": {{dev_dependencies}},
      "dependencies": {{dependencies}}
    }
    """)

    dev_dependencies = {
        "babel-core": "^6.5.0",
        "babel-loader": "^6.2.2",
        "babel-preset-es2015": "^6.5.0",
        "babel-preset-react": "^6.5.0",
        "bower": "^1.7.7",
        "css-loader": "^0.23.1",
        "d3": "^3.5.16",
        "jquery": "^2.2.0",
        "node-sass": "^3.3.3",
        "nvd3": "^1.8.2",
        "datamaps": "^0.4.4",
        "metrics-graphics": "^2.8.0",
        "datatables": "^1.10.7",
        "plotly.js": "^1.5.2",
        "react": "^0.14.7",
        "react-bootstrap": "^0.28.3",
        "react-dom": "^0.14.7",
        "react-router": "^2.0.0",
        "sass-loader": "^3.1.2",
        "style-loader": "^0.13.0",
        "webpack": "^1.12.13",
        "webpack-dev-server": "^1.14.1",
        "pyxley": "^0.0.6"
    }
    def __init__(self, repo_root):
        self.repo_root = repo_root

    def create_package_json(self,
            name="PyxleyApp",
            version="0.0.1",
            main="index.js",
            dependencies={},
            scripts={}):
        """
        """

        if "build" not in scripts:
            _build = "node_modules/.bin/webpack"
            scripts["build"] = _build

        options = {
            "name": name,
            "version": version,
            "main": main,
            "scripts": json.dumps(scripts),
            "dependencies": json.dumps(dependencies),
            "dev_dependencies": json.dumps(self.dev_dependencies)
        }

        rt = ReactTemplate(self.package_template,
            options, self.repo_root+"/package.json")
        rt.to_js()

    def run(self):
        # check repo root for a package.json file
        if not os.path.isfile(self.repo_root+"/package.json"):
            print("Creating package.json...", file=sys.stderr)
            self.create_package_json()


        cmds = ["npm", "install", "--progress-false"]
        try:
            run(cmds, cwd=self.repo_root)
        except OSError as e:
            print("Failed to run `npm install`: %s" % e, file=sys.stderr)
            print("npm is required to build a pyxley app", file=sys.stderr)
            raise
