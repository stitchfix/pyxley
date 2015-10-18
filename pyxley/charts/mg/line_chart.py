from .mg import MG
from flask import jsonify, request

class LineChart(MG):
    """Wrapper for MetricsGraphics Line plot.

        https://github.com/mozilla/metrics-graphics/wiki/Chart-Types
        The user must supply a Figure object. When a route_func
        is supplied, the dataframe and other options are ignored
        in favor of the endpoint function.

        Args:
            df (dataframe): input data.
            figure (mg.Figure): metricsgraphics figure object.
            x (str): name of the column corresponding to the x-axis.
            y (str): name of the column corresponding to the y-axis.
            title (str): title of the figure.
            description (str): description of the figure.
            init_params (dict): parameters used to initialize the figure.
            timeseries (bool): inidicates whether the plot is a timeseries.
            route_func (function): endpoint function.

    """
    def __init__(self, df, figure, x, y, title="Line Chart",
        description="Line Chart", init_params={}, timeseries=False,
        route_func=None):

        self.plot_opts = {
            "title": title,
            "description": description,
            "target": "#"+figure.chart_id,
            "x_accessor": "x",
            "y_accessor": "y",
            "init_params": init_params
        }
        for k, v in list(figure.get().items()):
            self.plot_opts[k] = v

        if not route_func:
            def get_data():
                args = {}
                for c in init_params:
                    if request.args.get(c):
                        args[c] = request.args[c]
                    else:
                        args[c] = init_params[c]
                return jsonify(LineChart.to_json(
                        self.apply_filters(df, args),
                        x,
                        y,
                        timeseries=timeseries
                    ))
            route_func = get_data

        super(LineChart, self).__init__(figure.chart_id, figure.url, self.plot_opts, route_func)

    @staticmethod
    def to_json(df, x, y, timeseries=False):
        """Format output for json response."""
        values = {k: [] for k in y}
        for i, row in df.iterrows():
            for yy in y:
                values[yy].append({
                    "x": row[x],
                    "y": row[yy]
                    })
        return {"result":  [values[k] for k in y], "date": timeseries}
