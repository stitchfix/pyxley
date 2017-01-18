
from ..charts import Chart
from flask import jsonify, request

_BASE_CONFIG = {
    "showLink": False,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["sendDataToCloud"]
}

class PlotlyAPI(Chart):
    """ Base class for Plotly.js API

        This class is used to create charts using the plotly.js api

        To keep this general, this chart does not have a default
        method of transmitting data. Instead the user must supply
        a route_func method.

    """

    def __init__(self, chart_id, url, route_func, init_params={}):

        options = {
            "chartid": chart_id,
            "url": url,
            "params": init_params
        }
        super(PlotlyAPI, self).__init__("PlotlyAPI", options, route_func)

    @staticmethod
    def line_plot(df, xypairs, mode, layout={}, config=_BASE_CONFIG):
        """ basic line plot

            dataframe to json for a line plot

            Args:
                df (pandas.DataFrame): input dataframe
                xypairs (list): list of tuples containing column names
                mode (str): plotly.js mode (e.g. lines)
                layout (dict): layout parameters
                config (dict): config parameters
        """
        if df.empty:
            return {
                "x": [],
                "y": [],
                "mode": mode
            }

        _data = []
        for x, y in xypairs:
            if (x in df.columns) and (y in df.columns):
                _data.append(
                    {
                        "x": df[x].values.tolist(),
                        "y": df[y].values.tolist(),
                        "mode": mode
                    }
                )

        return {
            "data": _data,
            "layout": layout,
            "config": config
            }
