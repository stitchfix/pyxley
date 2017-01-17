# datatables.js Example
This example shows off the integration of the [DataTables](https://www.datatables.net/) jQuery plug-in. In addition, we are able to use d3 to render intervals. The data comes from the DataTables examples on their website.

## What's In Here?

This example showcases the flexibility of the
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

## Static Files
In this example, we need to include some additional javascript files.
Rather than serving the default static directory, we are going to
copy the pyxley bundle into our own static folder. This is achieved
with the following code:

```python
import shutil
def check_for_bundle(path_to_static):
    # check if bundle.js exists
    if not path.isfile(path_to_static+"/bundle.js"):
        # grab the bundle
        _path_to_bundle = default_static_path() + "/bundle.js"
        shutil.copy2(_path_to_bundle, path_to_static)
```
It simply looks for `bundle.js` using the provided `path_to_static`
variable and if it can't find the file, it copies it from
`pyxley.utils.default_static_path`.

Because we will be serving files that are different from the defaults
we include our own index routing function and flask html template file.

# Run the App
Run `python project/__init__.py`.
