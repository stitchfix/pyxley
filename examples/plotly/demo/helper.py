
from pyxley.charts import Chart
from flask import jsonify, request

class PlotlyAPI(Chart):
    def __init__(self, options, route_func):
        super(PlotlyAPI, self).__init__("PlotlyAPI", options, route_func)

class PlotlyLines(PlotlyAPI):
    def __init__(self, xypairs, data_source,
        mode="lines+markers", layout={},
        init_params={},
        chart_id="plotlyid", url="/plotlyurl/",
        route_func=None):

        self.options = {
            "chartid": chart_id,
            "url": url,
            "params": init_params
        }
        def get_data():
            args = {}
            for c in init_params:
                if request.args.get(c):
                    args[c] = request.args[c]
                else:
                    args[c] = init_params[c]
            return jsonify(PlotlyLines.to_json(
                    self.apply_filters(data_source, args),
                    xypairs,
                    mode,
                    layout
                ))
        if not route_func:
            route_func = get_data

        super(PlotlyLines, self).__init__(self.options, route_func)

    @staticmethod
    def to_json(df, xypairs, mode, layout):
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
            "layout": layout
            }
