from components.filters import *
from components.metricsgraphics import make_mg_layout
from pyxley import UILayout

def build_filter_props(buttons):
    """ build filter props

        return props for a list of buttons.

        Args:
            buttons (list): list of pyxley.Filter components.
    """
    ui = UILayout(
        "FilterChart",
        "pyxley",
        "component_id")

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
    for p in _props["filters"]:
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
    return [
        filters_only,
        mg_props
    ]
