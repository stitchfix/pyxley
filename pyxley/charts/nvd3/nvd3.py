from ..charts import Chart

class NVD3(Chart):
    """Base class for NVD3 Charts.

        This class is used to create charts from http://nvd3.org/

    """
    def __init__(self, opts, api_route):
        super(NVD3, self).__init__("NVD3Chart", opts, api_route)
