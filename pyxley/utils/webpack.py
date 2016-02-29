
from __future__ import print_function

import os
import sys
import json

from ..react_template import ReactTemplate
from .npm import run
from subprocess import check_call

class Webpack(object):
    webpack_template = """
        var path = require("path");
        var webpack = require("webpack");

        module.exports = {
          entry: [
              '{{include_path}}/{{entry_point}}'
          ],
          output: {
            path: path.join(__dirname,'{{output_path}}'),
            sourceMapFilename: '{{output_name}}.map',
            filename: '{{output_name}}.js'
          },
          resolve: {
              extensions: ['', '.js', '.scss'],
              alias: {
                  react: path.resolve('./node_modules/react')
              }
          },

          module: {
            loaders: [
              {
                test: /\.js?$/,
                include: path.join(__dirname,'{{include_path}}'),
                loader: ['babel-loader'],
                exclude: /node_modules/,
                query: {
                    presets: ['es2015', 'react']
                }
              },
              {
                test: /\.scss$/,
                loaders: ['style', 'css', 'sass']
              },
              {
                test: /\.json$/,
                loader: 'json'
              }
            ]
        },
        plugins: [
                new webpack.ProvidePlugin({
                  $: "jquery",
                  jQuery: "jquery",
                  MG: "metrics-graphics",
                  Datamap: "datamaps",
                  Plotly: "plotly.js",
                  nv: "nvd3"
                })
            ]
        };
    """

    def __init__(self, repo_root):
        self.repo_root = repo_root

    def create_webpack_config(self, main_js, include_path,
        output_name, output_path):

        options = {
            "entry_point": main_js,
            "include_path": include_path,
            "output_name": output_name,
            "output_path": output_path
        }
        rt = ReactTemplate(self.webpack_template,
            options, self.repo_root+"/webpack.config.js")
        rt.to_js()


    def run(self):

        # check repo root for a package.json file
        if not os.path.isfile(self.repo_root+"/webpack.config.js"):
            print("Creating webpack.config.js...", file=sys.stderr)
            self.create_webpack_config("index.js", ".", "bundle", ".")

        try:
            run(["npm", "run-script", "build"], cwd=self.repo_root)
        except Exception as e:
            print("Failed to run `npm run-script build`: %s" % e, file=sys.stderr)
            print("Please resolve javascript errors", file=sys.stderr)
            print("Try running with --display-error-details")
            raise
