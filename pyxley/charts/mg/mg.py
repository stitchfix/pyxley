from ..charts import Chart

class MG(Chart):
    """Base class for MetricsGraphics API.

        This class creates a MetricsGraphics component based on the supplied
        options.
        https://github.com/mozilla/metrics-graphics/wiki/List-of-Options

        Args:
            chart_id (str): html element id.
            url (str): name of the endpoint to create.
            params (dict): parameters and options of the chart.
            api_route (function): endpoint function.
    """
    def __init__(self, chart_id, url, params, api_route):
        opts = {
            "url": url,
            "chart_id": chart_id,
            "params": params
        }
        super(MG, self).__init__("MetricsGraphics", opts, api_route)

class OptionHelper(object):
    """Option Base class for the MetricsGraphics API."""
    def __init__(self):
        self.options = {}

    def set_float(self, option, value):
        """Set a float option.

            Args:
                option (str): name of option.
                value (float): value of the option.

            Raises:
                TypeError: Value must be a float.
        """
        if not isinstance(value, float):
            raise TypeError("Value must be a float")
        self.options[option] = value

    def set_integer(self, option, value):
        """Set an integer option.

            Args:
                option (str): name of option.
                value (int): value of the option.

            Raises:
                ValueError: Value must be an integer.
        """
        try:
            int_value = int(value)
        except ValueError as err:
            print(err.args)

        self.options[option] = value

    def set_boolean(self, option, value):
        """Set a boolean option.

            Args:
                option (str): name of option.
                value (bool): value of the option.

            Raises:
                TypeError: Value must be a boolean.
        """
        if not isinstance(value, bool):
            raise TypeError("%s must be a boolean" % option)

        self.options[option] = str(value).lower()

    def set_string(self, option, value):
        """Set a string option.

            Args:
                option (str): name of option.
                value (str): value of the option.

            Raises:
                TypeError: Value must be a string.
        """
        if not isinstance(value, str):
            raise TypeError("%s must be a string" % option)

        self.options[option] = value


