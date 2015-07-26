from .mg import MG
from flask import jsonify, request

class LineChart(MG):
    def __init__(self, df, figure, x, y, title="Line Chart",
        description="Line Chart", init_params={}, timeseries=False):

        self.x = x
        self.y = y
        self.plot_opts = {
            "title": title,
            "description": description,
            "target": "#"+figure.chart_id,
            "x_accessor": "x",
            "y_accessor": "y",
            "init_params": init_params
        }
        self.timeseries = timeseries
        for k, v in list(figure.get().items()):
            self.plot_opts[k] = v

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

        super(LineChart, self).__init__(figure.chart_id, figure.url, self.plot_opts, get_data)

    def to_json(self, df):
        values = [[]]*len(self.y)
        values = {k: [] for k in self.y}
        for i, row in df.iterrows():
            for yy in self.y:
                values[yy].append({
                    "x": row[self.x],
                    "y": row[yy]
                    })
        return {"result":  [values[k] for k in self.y], "date": self.timeseries}
