
import pandas as pd

from pyxley import UILayout
from pyxley.filters import SelectButton

from helper import PlotlyLines

def make_ui(datafile):
    # Make a UI
    ui = UILayout(
        "FilterChart",
        "pyxley",
        "component_id",
        filter_style="''")

    df = pd.read_csv(datafile)

    # Read in the data and stack it, so that we can filter on columns
    sf = df.set_index("Date").stack().reset_index()
    sf = sf.rename(columns={"level_1": "Data", 0: "value"})

    # Make a Button
    cols = [c for c in df.columns if c != "Date"]
    btn = SelectButton("Data", cols, "Data", "Steps")

    # Make a FilterFrame and add the button to the UI
    ui.add_filter(btn)

    dm = PlotlyLines([["Date", "value"]], sf,
        init_params={"Data": "Steps"})
    ui.add_chart(dm)
    return ui
