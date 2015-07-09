# datatables.js Example
This example shows off the integration of the [DataTables](https://www.datatables.net/) jQuery plug-in. In addition, we are able to use d3 to render intervals. The data comes from the DataTables examples on their website.

## What's In Here?
This example showcases the use of a the `SingleComponent` class as well as combining existing extensions (such as `FixedColumns`). The d3 rendering function was provided by Andrew Almand-Hunter.

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



