from ..charts import Chart

class NVD3(Chart):
    def __init__(self, opts, api_route):
        super(NVD3, self).__init__("NVD3Chart", opts, api_route)
