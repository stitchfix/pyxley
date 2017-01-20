from components.filters import *
from components.metricsgraphics import make_mg_layout
from components.plotly import make_plotly_ui
from components.datamaps import make_datamaps_ui
from components.datatables import make_table_layout
from components.nvd3 import make_nv_layout

from collections import OrderedDict

from pyxley import UILayout, register_layouts

def build_filter_props(buttons):
    """ build filter props

        return props for a list of buttons.

        Args:
            buttons (list): list of pyxley.Filter components.
    """
    ui = UILayout("PyxleyChart")

    for b in buttons:
        ui.add_filter(b)

    return ui.build_props()

def get_filter_props():
    _buttons = [
        get_select_button(),
        get_api_button(),
        get_slider_input(),
        get_download_button(),
        get_react_select()
    ]
    _props = build_filter_props(_buttons)

    # let's add a label to each of the filters

    for grp in _props["filters"]:
        _filters = _props["filters"][grp]
        for p in _filters:
            p["label"] = p["type"]

    return _props

def get_layouts(mod):

    # filters only
    filters_only = get_filter_props()
    filters_only["charts"] = []
    filters_only["title"] = "Filters"

    # metrics graphics
    mg_ui = make_mg_layout()
    mg_ui.assign_routes(mod)
    mg_props = mg_ui.build_props()
    mg_props["title"] = "Metricsgraphics"

    # plotly
    plotly_ui = make_plotly_ui()
    plotly_ui.assign_routes(mod)
    plotly_props = plotly_ui.build_props()
    plotly_props["title"] = "Plotly.js"

    # datamaps
    dm_ui = make_datamaps_ui()
    dm_ui.assign_routes(mod)
    dm_props = dm_ui.build_props()
    dm_props["title"] = "Datamaps"

    # datatables
    dt_ui = make_table_layout()
    dt_ui.assign_routes(mod)
    dt_props = dt_ui.build_props()
    dt_props["title"] = "Datatables"

    # nvd3
    nv_ui = make_nv_layout()
    nv_ui.assign_routes(mod)
    nv_props = nv_ui.build_props()
    nv_props["title"] = "NVD3"

    _layouts = OrderedDict()
    _layouts["filters"] = {"layout": [filters_only], "title": "Filters"}
    _layouts["mg"] = {"layout": [mg_props], "title": "metrics-graphics"}
    _layouts["plotly"] = {"layout": [plotly_props], "title": "Plotly"}
    _layouts["datamaps"] = {"layout": [dm_props], "title": "Datamaps"}
    _layouts["datatables"] = {"layout": [dt_props], "title": "Datatables"}
    _layouts["nvd3"] = {"layout": [nv_props], "title": "NVD3"}

    register_layouts(_layouts, mod)
