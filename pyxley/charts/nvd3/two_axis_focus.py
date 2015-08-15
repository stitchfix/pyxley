
from .nvd3 import NVD3
from flask import jsonify, request
import numpy as np

class TwoAxisFocus(NVD3):
    _allowed_axes = ["sigma", "minmax"]
    def __init__(self, x, y1, y2, data_source, init_params={},
        chart_id="new_chart", url="/new_chart/", colors=[], auto_scale="sigma",
        y1_axis_range=[], y2_axis_range=[], sigma=3,
        x_label="", y1_label="", y2_label="",
        margin={"top": 30, "right": 60, "bottom": 50, "left": 70}):

        self.x = x
        self.y1 = y1
        self.y2 = y2
        self.auto_scale = auto_scale if auto_scale in self._allowed_axes else "sigma"
        self.sigma = 3
        self.y1_axis_range = y1_axis_range
        self.y2_axis_range = y2_axis_range

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
        def get_data():
            args = {}
            for c in init_params:
                if request.args.get(c):
                    args[c] = request.args[c]
                else:
                    args[c] = init_params[c]
            return jsonify(self.to_json(
                    self.apply_filters(data_source, args)
                ))

        super(TwoAxisFocus, self).__init__(self.options, get_data)

    def get_bounds(self, y, method="sigma"):
        if self.auto_scale == "sigma":
            m_, s_ = y.mean(), y.std()
            l = m_ - self.sigma*s_
            u = m_ + self.sigma*s_
        else:
            l = y.min()
            u = y.max()
        return [l, u]

    def to_json(self, df):
        if df.empty:
            return {
                "data": [],
                "yAxis1": {"lower": 0, "upper": 1},
                "yAxis2": {"lower": 0, "upper": 1}
            }

        if not self.y1_axis_range:
            bounds1 = self.get_bounds(df[self.y1], method=self.auto_scale)
        else:
            bounds1 = self.y1_axis_range

        if not self.y2_axis_range:
            bounds2 = self.get_bounds(df[self.y2], method=self.auto_scale)
        else:
            bounds2 = self.y2_axis_range

        records = [
            {"key": self.y1, "values": [], "yAxis": 1, "type": "line"},
            {"key": self.y2, "values": [], "yAxis": 2, "type": "line"}
        ]

        for n, r in df.iterrows():
            records[0]["values"].append({"x": r[self.x], "y": r[self.y1]})
            records[1]["values"].append({"x": r[self.x], "y": r[self.y2]})

        return {
            "data": records,
            "yAxis1": {"bounds": bounds1},
            "yAxis2": {"bounds": bounds2}
            }
