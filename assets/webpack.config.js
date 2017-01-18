
        var path = require("path");
        var webpack = require("webpack");

        module.exports = {
          entry: [
              './jsx/layout.js'
          ],
          output: {
            path: path.join(__dirname,'./'),
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
                include: path.join(__dirname,'./'),
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
                  d3: "d3",
                  MG: "metrics-graphics",
                  Datamap: "datamaps",
                  nv: "nvd3"
              }),
              new webpack.DefinePlugin({
                  "process.env": {
                    NODE_ENV: JSON.stringify("production")
                  }
              })
            ]
        };
