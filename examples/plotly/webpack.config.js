
        var path = require("path");
        var webpack = require("webpack");

        module.exports = {
          entry: [
              './demo/static//layout.js'
          ],
          output: {
            path: path.join(__dirname,'./demo/static/'),
            sourceMapFilename: 'bundle.map',
            filename: 'bundle.js'
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
                include: path.join(__dirname,'./demo/static/'),
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
    