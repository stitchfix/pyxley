import pandas as pd

from pyxley import UILayout
from pyxley.filters import SliderInput
from pyxley.charts.datamaps import DatamapUSA

def make_datamaps_ui():
    # Make a UI
    ui = UILayout(
        "PyxleyChart",
        "component_id")

    datafile = "../examples/datamaps/project/Colorful_State.csv"
    df = pd.read_csv(datafile)
    df.month = df.month.astype('str')

    sldr = SliderInput("Month", 1, 13, "month", "1")
    ui.add_filter(sldr)

    dm = DatamapUSA("/data_map/", "mapid", df,
        "state", "color1", init_params={"month": "1"})
    ui.add_chart(dm)
    return ui
