import pandas as pd
import re
import numpy as np
from collections import OrderedDict
from pyxley.charts.datatables import DataTable
from pyxley import UILayout, register_layouts

import json

def get_data(filename="./project/static/data.json"):
    df = pd.DataFrame(json.load(open(filename, "r")))
    df = df.dropna()

    # fix the salary column and cast as float
    df["salary"] = df["salary"].apply(lambda x: float(re.sub("[^\d\.]", "", x)))

    # make some random bounds
    _lower = ( 1. - (0.03*np.random.randn(df.shape[0]) + 0.15))
    _upper = ( 1. + (0.03*np.random.randn(df.shape[0]) + 0.15))
    df = df.assign(
        salary_upper = _upper * df.salary,
        salary_lower = _lower * df.salary
    )
    return df

def create_datatable(df, tablename="mytable"):
    cols = OrderedDict([
        ("position", {"label": "Position"}),
        ("office", {"label": "Office"}),
        ("start_date", {"label": "Start Date"}),
        ("salary_lower", {
            "label": "Salary Range",
            "confidence": {
                "lower": "salary_lower",
                "upper": "salary_upper"
            }
        })
    ])

    addfunc = (
    """
        confidence_interval(this.api().column(3,
            {{"page":"current"}}).data(), "{tablename}");
    """.format(tablename=tablename))

    drawfunc = (
    """
        confidence_interval(this.api().column(3,
            {{"page":"current"}}).data(), "{tablename}");
    """.format(tablename=tablename))

    _table = DataTable(tablename, "/api/{}/".format(tablename), df,
        columns=cols, paging=True, pageLength=9, scrollX=True,
        columnDefs=[{
            "render": """<svg width="156" height="20"><g></g></svg>""",
            "orderable": False,
            "targets": 3
        }],
        sDom='<"top">rt<"bottom"lp><"clear">', deferRender=True,
        initComplete=addfunc, drawCallback=drawfunc)

    return _table

def make_table_layout():
    filename = "../examples/datatables/project/static/data.json"
    df = get_data(filename)

    ui = UILayout("SimpleChart")
    ui.add_chart(create_datatable(df))
    return ui
