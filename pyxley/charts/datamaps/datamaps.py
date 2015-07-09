from ..charts import Chart
import pandas as pd
from flask import request, jsonify, make_response

_COLOR_MAP = {
    'light blue':'#add8e6',
    "antique gold":'#fff4b0',
    "antique silver":'#d7cdc4',
    "beige": '#f5f5dc',
    "black":'#000000',
    "blue": '#8084ff',
    "bronze": '#c95a0b',
    "brown": '#864',
    "burgundy": '#ff7272',
    "burnt orange": '#cc5500',
    "camel": '#c96',
    "canary yellow": '#ffef00',
    "cobalt": "#56b3ff",
    "coral": "#ff9e80",
    "dark green": '#006400',
    "dark grey": '#666666',
    "dark pink": '#e3489b',
    "dark purple": '#540061',
    "fuchsia": '#ff00ff',
    "gold": '#fc0',
    "gray": '#9c9c9c',
    "green": "#83ff7f",
    "grey": "#9c9c9c",
    "jewel tone purple": '#ae2cc6',
    "light green": '#90ee90',
    "light grey": '#d3d3d3',
    "light pink": '#ffd6d3',
    "light purple": '#b0c4de',
    "magenta":  '#ff00ff',
    "mustard":  '#ffe761',
    "navy": '#6c70ff',
    "off-white": '#ffffdd',
    "olive": '#808000',
    "orange": '#ffc870',
    "orange red": '#ff4500',
    "pale yellow": '#ffff9d',
    "pink": '#ffb6c1',
    "purple": '#800080',
    "red": '#ff0000',
    "rose gold": '#ffba9d',
    "silver": '#c0c0c0',
    "soft orange": '#ffc63c',
    "tan":  '#d2b48c',
    "teal": '#008080',
    "teal green":'#a1dfc6',
    "turquoise": '#40e0d0',
    "white": '#ffffff',
    "yellow": '#ffff00',
    "other": '#111111'
}

class Datamap(Chart):
    def __init__(self, chart_id, url, params, api_route):
        opts = {
            "url": url,
            "chartid": chart_id,
            "params": params
        }
        super(Datamap, self).__init__("Datamaps", opts, api_route)

class DatamapUSA(Datamap):
    def __init__(self, url, chart_id, df,
                state_index, color_index,
                init_params={},
                color_map=_COLOR_MAP):

        self.state_index = state_index
        self.color_index = color_index
        self.fills = color_map
        self.fills["defaultFills"] = "black"

        def get_data():
            args = {}
            for c in init_params:
                if request.args.get(c):
                    args[c] = request.args[c]
                else:
                    args[c] = init_params[c]
            return jsonify(self.to_json(
                    self.apply_filters(df, args)
                ))
        super(DatamapUSA, self).__init__(chart_id, url, init_params, get_data)

    def to_json(self, df):
        records = {}
        for i, row in df.iterrows():

            records[row[self.state_index]] = {
                "fillKey": row[self.color_index]
            }

        return {
            "data": records,
            "fills": self.fills
        }
