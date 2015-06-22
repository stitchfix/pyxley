
from mg import MG

class Histogram(MG):
    def __init__(self, data_source, figure, column, bins, title="Histogram",
        description="Histogram", init_params={}):
        self.column = column
        self.plot_opts = {
            "title": title,
            "description": description,
            "init_params": init_params,
            "bins": bins
        }
        figure.graphics.chart_type("histogram")
        figure.graphics.target("#"+figure.chart_id)
        for k, v in figure.get().items():
            self.plot_opts[k] = v
        data_source.to_json = self.to_json
        super(Histogram, self).__init__(figure.chart_id, figure.url,
            self.plot_opts, data_source)

    def to_json(self, df):
        return {"result": df[self.column].tolist()}

