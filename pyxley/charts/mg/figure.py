from .axes import Axes
from .layout import Layout
from .graphic import Graphic

class Figure(object):
    def __init__(self, url, chart_id):
        self.url = url
        self.chart_id = chart_id
        self.axes = Axes()
        self.graphics = Graphic()
        self.layout = Layout()

    def get(self):
        options = {}
        for x in [self.axes, self.graphics, self.layout]:
            for k, v in list(x.get().items()):
                options[k] = v

        return options

