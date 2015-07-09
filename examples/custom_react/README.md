# Custom React Example
This example demonstrates integrating custom react components. For simplicity, we've created a parent UI component that mirrors the Pyxley `FilterChart` component.

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

## NV-D3
This example uses a modified `NV-D3` chart containing a dual-axis line plot with a focus chart. It is adapted from the [Line Chart with View Finder example](http://nvd3.org/examples/lineWithFocus.html).




