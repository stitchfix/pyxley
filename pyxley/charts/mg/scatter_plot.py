
from .mg import MG

class ScatterPlot(MG):
    def __init__(self, df, figure, x, y, title="Scatter Plot",
        description="Scatter Plot", init_params={}):
        self.x = x
        self.y = y
        self.plot_opts = {
            "title": title,
            "description": description,
            "x_accessor": "x",
            "y_accessor": "y",
            "init_params": init_params
        }
        figure.graphics.chart_type("point")
        figure.graphics.target("#"+figure.chart_id)
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
        super(ScatterPlot, self).__init__(figure.chart_id, figure.url,
            self.plot_opts, get_data)

    def to_json(self, df):
        values = []
        for i, row in df.iterrows():
            values.append({
                "x": row[self.x],
                "y": row[self.y]
                })
        return {"result": values}

