
from .nvd3 import NVD3
from flask import jsonify, request
import numpy as np

class TwoAxisFocus(NVD3):
    """NVD3 Two Axis Focus

        Wrapper for the cross-filter chart implemented in PyxleyJS based on
        http://nvd3.org/examples/linePlusBar.html. When a route_func is supplied,
        the inputs are ignored in favor of the endpoint function.

        Args:
            values (dict): labels of the pie chart.
            data_source (dataframe): chart data.
            x (str): name of the column for the x-axis.
            y1 (str): name of the column for the primary y-axis.
            y2 (str): name of the column for the secondary y-axis.
            init_params (dict): parameters used to initialize the chart.
            chart_id: html element id.
            url: name of the endpoint to be created.
            colors (list): list of colors to show in the chart.
            auto_scale (str): select auto scale method.
            y1_axis_range (list): range of the primary y-axis.
            y2_axis_range (list): range of the secondary y-axis.
            x_label (str): label of the x-axis.
            y1_label (str): label of the primary axis.
            y2_label (str): label of the secondary axis.
            margin (dict): margins in pixels.
            route_func (function): optional endpoint function.

    """
    _allowed_axes = ["sigma", "minmax"]
    def __init__(self, x, y1, y2, data_source, init_params={},
        chart_id="new_chart", url="/new_chart/", colors=[], auto_scale="sigma",
        y1_axis_range=[], y2_axis_range=[], sigma=3,
        x_label="", y1_label="", y2_label="",
        margin={"top": 30, "right": 60, "bottom": 50, "left": 70},
        route_func=None):


        self.auto_scale = auto_scale if auto_scale in self._allowed_axes else "sigma"

        self.options = {
            "type": "TwoAxisFocus",
            "chartid": chart_id,
            "url": url,
            "colors": colors,
            "init_params": init_params,
            "labels": {
                "xAxis": x_label,
                "yAxis1": y1_label,
                "yAxis2": y2_label
            },
            "margin": margin,
            "type": "TwoAxisFocus"
        }
        if not route_func:
            def get_data():
                args = {}
                for c in init_params:
                    if request.args.get(c):
                        args[c] = request.args[c]
                    else:
                        args[c] = init_params[c]
                return jsonify(self.to_json(
                        self.apply_filters(data_source, args),
                        x, y1, y2, y1_axis_range, y2_axis_range,
                        self.auto_scale, sigma
                    ))
            route_func = get_data

        super(TwoAxisFocus, self).__init__(self.options, route_func)

    @staticmethod
    def get_bounds(y, method="sigma", sigma=3):
        if method == "sigma":
            m_, s_ = y.mean(), y.std()
            l = m_ - sigma*s_
            u = m_ + sigma*s_
        else:
            l = y.min()
            u = y.max()
        return [l, u]

    @staticmethod
    def to_json(df, x, y1, y2, y1_axis_range, y2_axis_range, auto_scale, sigma):
        if df.empty:
            return {
                "data": [],
                "yAxis1": {"lower": 0, "upper": 1},
                "yAxis2": {"lower": 0, "upper": 1}
            }

        if not y1_axis_range:
            bounds1 = TwoAxisFocus.get_bounds(df[y1], method=auto_scale, sigma=sigma)
        else:
            bounds1 = y1_axis_range

        if not y2_axis_range:
            bounds2 = TwoAxisFocus.get_bounds(df[y2], method=auto_scale, sigma=sigma)
        else:
            bounds2 = y2_axis_range

        records = [
            {"key": y1, "values": [], "yAxis": 1, "type": "line"},
            {"key": y2, "values": [], "yAxis": 2, "type": "line"}
        ]

        for n, r in df.iterrows():
            records[0]["values"].append({"x": r[x], "y": r[y1]})
            records[1]["values"].append({"x": r[x], "y": r[y2]})

        return {
            "data": records,
            "yAxis1": {"bounds": bounds1},
            "yAxis2": {"bounds": bounds2}
            }
