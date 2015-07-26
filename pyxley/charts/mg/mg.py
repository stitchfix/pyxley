from ..charts import Chart

class MG(Chart):
    def __init__(self, chart_id, url, params, api_route):
        opts = {
            "url": url,
            "chart_id": chart_id,
            "params": params
        }
        super(MG, self).__init__("MetricsGraphics", opts, api_route)

class OptionHelper(object):
    def __init__(self):
        self.options = {}

    def set_float(self, option, value):
        if not isinstance(value, float):
            raise TypeError("Inflator must be a float")
        self.options[option] = value

    def set_integer(self, option, value):
        try:
            int_value = int(value)
        except ValueError as err:
            print(err.args)

        self.options[option] = value

    def set_boolean(self, option, value):
        if not isinstance(value, bool):
            raise TypeError("%s must be a boolean" % option)

        self.options[option] = str(value).lower()

    def set_string(self, option, value):
        if not isinstance(value, str):
            raise TypeError("%s must be a string" % option)

        self.options[option] = value


