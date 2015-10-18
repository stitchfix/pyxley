
from .mg import MG
from flask import jsonify, request

class Histogram(MG):
    """Wrapper for MetricsGraphics Histogram plot.

        https://github.com/mozilla/metrics-graphics/wiki/Histogram
        The user must supply a Figure object. When a route_func
        is supplied, the dataframe and other options are ignored
        in favor of the endpoint function.

        Args:
            df (dataframe): input data.
            figure (mg.Figure): metricsgraphics figure object.
            column (str): name of the column to histogram.
            bins (int): number of bins.
            title (str): title of the figure.
            description (str): description of the figure.
            init_params (dict): parameters used to initialize the figure.
            route_func (function): endpoint function.

    """
    def __init__(self, df, figure, column, bins, title="Histogram",
        description="Histogram", init_params={}, route_func=None):

        self.plot_opts = {
            "title": title,
            "description": description,
            "init_params": init_params,
            "bins": bins
        }
        figure.graphics.chart_type("histogram")
        figure.graphics.target("#"+figure.chart_id)
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
                return jsonify(Histogram.to_json(
                        self.apply_filters(df, args),
                        column
                    ))
            route_func = get_data

        super(Histogram, self).__init__(figure.chart_id, figure.url,
            self.plot_opts, route_func)

    @staticmethod
    def to_json(df, column):
        """Format output for json response."""
        return {"result": df[column].tolist()}

