from .nvd3 import NVD3
from flask import jsonify, request
import numpy as np

class PieChart(NVD3):
    def __init__(self, values, df, init_params={},
        chart_id="piechart", url="/piechart/", colors=[]):

        self.options = {
            "type": "PieChart",
            "chartid": chart_id,
            "url": url,
            "colors": colors
        }

        self.values = values
        def get_data():
            args = {}
            for c in init_params:
                if request.args.get(c):
                    args[c] = request.args[c]
                else:
                    args[c] = init_params[c]
            return jsonify(self.to_json(
                        self.apply_filters(df, args)
                    ))

        super(PieChart, self).__init__(self.options, get_data)

    def to_json(self, df):

        records = []
        sum_ = np.sum([df[c].iloc[0] for c in self.values])
        for c in self.values:
            records.append({
                "label": self.values[c],
                "value": "%.2f"%np.around(df[c].iloc[0] / sum_, decimals=2)
                })
        return {
            "data" : records
        }
