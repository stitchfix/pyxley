from .nvd3 import NVD3
from flask import jsonify, request
import numpy as np

class PieChart(NVD3):
    """NVD3 Pie Chart

        Wrapper for the NVD3 pie chart implemented in PyxleyJS based on
        http://nvd3.org/examples/pie.html. When a route_func is supplied,
        the inputs are ignored in favor of the endpoint function.

        Args:
            values (dict): labels of the pie chart.
            df (dataframe): chart data.
            init_params (dict): parameters used to initialize the chart.
            chart_id: html element id.
            url: name of the endpoint to be created.
            colors (list): list of colors to show in the chart.
            label_type (str): type of label to display.
            route_func (function): optional endpoint function.

    """
    _allowed = ["key", "value", "percent"]
    def __init__(self, values, df, init_params={},
        chart_id="piechart", url="/piechart/", colors=[],
        label_type="percent", route_func=None):

        if label_type not in self._allowed:
            label_type = "percent"

        self.options = {
            "type": "PieChart",
            "chartid": chart_id,
            "url": url,
            "colors": colors,
            "init_params": init_params,
            "labelType": label_type
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
                            self.apply_filters(df, args),
                            values
                        ))
            route_func = get_data

        super(PieChart, self).__init__(self.options, route_func)

    @staticmethod
    def to_json(df, values):
        """Format output for the json response."""
        records = []
        if df.empty:
            return {"data": []}

        sum_ = float(np.sum([df[c].iloc[0] for c in values]))
        for c in values:
            records.append({
                "label": values[c],
                "value": "%.2f"%np.around(df[c].iloc[0] / sum_, decimals=2)
                })
        return {
            "data" : records
        }
