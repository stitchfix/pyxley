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
    "other": '#111111',
    "defaultFills": "black"
}

class Datamap(Chart):
    """ Pyxley Datamaps Chart component.

        This is the base class for the PyxleyJS Datamaps wrapper.

        Args:
            url: name of endpoint to transmit data.
            chart_id: html element id.
            params: parameters chart will be initialized with.
            route_func: function called by the endpoint

    """
    def __init__(self, chart_id, url, params, api_route):
        opts = {
            "url": url,
            "chartid": chart_id,
            "params": params
        }
        super(Datamap, self).__init__("Datamaps", opts, api_route)

class DatamapUSA(Datamap):
    """ Wrapper for PyxleyJS Datamaps component.

        By default, this class builds a simple endpoint function.
        This can be overriden by supplying a route_func. When
        a route_func has been supplied, only the url, init_params,
        and route_func will be used.

        Args:
            url: name of endpoint to transmit data.
            chart_id: html element id.
            df: dataframe containing states and colors.
            state_index: column name of dataframe containing states.
            color_index: column name of dataframe containing colors.
            init_params: parameters chart will be initialized with.
            color_map: dictionary of color labels and hex values.
            route_func: function called by the endpoint. default is None


    """
    def __init__(self, url, chart_id, df,
                state_index, color_index,
                init_params={},
                color_map=_COLOR_MAP,
                route_func=None):

        if not route_func:
            def get_data():
                args = {}
                for c in init_params:
                    if request.args.get(c):
                        args[c] = request.args[c]
                    else:
                        args[c] = init_params[c]
                return jsonify(DatamapUSA.to_json(
                        self.apply_filters(df, args),
                            state_index,
                            color_index,
                            color_map
                    ))
            route_func = get_data

        super(DatamapUSA, self).__init__(chart_id, url, init_params, route_func)

    @staticmethod
    def to_json(df, state_index, color_index, fills):
        """Transforms dataframe to json response"""
        records = {}
        for i, row in df.iterrows():

            records[row[state_index]] = {
                "fillKey": row[color_index]
            }

        return {
            "data": records,
            "fills": fills
        }
