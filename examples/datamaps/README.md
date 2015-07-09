# datamaps.js Example
This example shows off the map featured in the MultiThreaded Blog: [The Most Colorful State](http://multithreaded.stitchfix.com/blog/2015/06/02/the-most-colorful-state/). It uses the [datamaps.js](http://datamaps.github.io/) Javascript library to create a choropleth map. Thanks to Zhou Yu and Eli Bressert for the data.


# How to Install
Make sure pyxley is installed first (run `python setup.py install`).

## NPM
Install NPM (e.g brew install node). Then run `npm install -g` in the directory containing
package.json. `-g` will make bower available globally.

### Bower
Create a file called `.bowerrc` containing
```json
{
    "directory": "./project/static/bower_components"
}
```
This will tell bower where to install the packages.

Now run `bower install` to install the bower components.

# Flask
Run `python app.py`.

