from .axes import Axes
from .layout import Layout
from .graphic import Graphic

class Figure(object):
    """ Metricsgraphics Figure class.

        This class is a composition of Axes, Graphic, and Layout options.

        Args:
            url (str): name of the endpoint to create.
            chart_id (str): html element id.

    """
    def __init__(self, url, chart_id):
        self.url = url
        self.chart_id = chart_id
        self.axes = Axes()
        self.graphics = Graphic()
        self.layout = Layout()

    def get(self):
        """Return axes, graphics, and layout options."""
        options = {}
        for x in [self.axes, self.graphics, self.layout]:
            for k, v in list(x.get().items()):
                options[k] = v

        return options

