# datatables.js Example
This example shows off the integration of the [DataTables](https://www.datatables.net/) jQuery plug-in. In addition, we are able to use d3 to render intervals. The data comes from the DataTables examples on their website.

## What's In Here?
While this example uses the DataTables.js library, it is
meant to highlight two capabilities:

1. How to use the `SingleComponent` class  
2. Including additional JavaScript for DataTables callbacks  

The `SingleComponent` class is meant to be used when there
are no need for filters. In the other apps, we bind an
entire layout to a single `div` element. Instead, we will bind
only a single Pyxley component.

In addition, this example showcases the flexibility of the
DataTables api. It accepts callback functions that allow us
to include other functionality. This example uses the
`FixedColumns` extension as well as additional `svg` rendering
of d3 (provided by Andrew Almand-Hunter).

### `initComplete`
The `initComplete` keyword argument can be used to pass the
JavaScript dataTables API a string containing further
instructions after the table has been initialized. In the example,
we create the following string:

```python
addfunc = """
new $.fn.dataTable.FixedColumns(this, {
    leftColumns: 1,
    rightColumns: 0
});
confidence_interval(this.api().column(3, {"page":"current"}).data(), "mytable");
"""
```

In the string, we call the function that initializes the
`FixedColumns` extension and we call the d3 rendering
function that draws confidence intervals.

# Installing 
Make sure pyxley is installed first (run `python setup.py install`).

## NPM
Install NPM (e.g brew install node).

## Webpack
This app has a custom webpack file. Rather than building
the `webpack.config.js` the app uses the one in the top-level
folder.

Simple install the `node_modules` with
`npm install`

# Flask
Run `python project/app.py`.
