from ..ui import UIComponent
import pandas as pd
from flask import request, jsonify, make_response

class Chart(UIComponent):
    name = "Chart"

class LinePlot(Chart):
    def __init__(self, chart_id, url, plot_object):
        opts = {
            "url": url,
            "chartid": chart_id
        }
        super(LinePlot, self).__init__("LinePlot", opts, plot_object.api_route)
