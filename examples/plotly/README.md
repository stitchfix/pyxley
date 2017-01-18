# Plot.ly example

## How To Run
Run `python project/__init__.py`.

## What's In Here?
This app demonstrates how to use the `PlotlyAPI` chart type. It uses
the `PlotlyAPI.line_plot` method to transform data from a `pandas.DataFrame`
into a simple line plot.

Unlike other charts, this api does not have a default method for
transmitting the data from the `DataFrame`. Instead, it is supplied in
the function `project/buildui.py`.
