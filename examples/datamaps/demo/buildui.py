import pandas as pd

from pyxley import UILayout, register_layouts
from pyxley.filters import SliderInput
from pyxley.charts.datamaps import DatamapUSA

def make_datamaps_ui(filename):
    # Make a UI
    ui = UILayout(
        "FilterChart",
        "component_id")

    df = pd.read_csv(filename)
    df.month = df.month.astype('str')

    sldr = SliderInput("Month", 1, 13, "month", "1")
    ui.add_filter(sldr)

    dm = DatamapUSA("/data_map/", "mapid", df,
        "state", "color1", init_params={"month": "1"})
    ui.add_chart(dm)
    return ui

def get_layouts(mod, filename):
    # datamaps
    dm_ui = make_datamaps_ui(filename)
    dm_ui.assign_routes(mod)
    dm_props = dm_ui.build_props()

    _layouts = {
        "datamaps": {"layout": [dm_props], "title": "Datamaps"}
    }
    register_layouts(_layouts, mod)
