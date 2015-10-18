from ..charts import Chart
from flask import jsonify, request


class DataTable(Chart):
    """Wrapper for jquery DataTables.

        This class provides a wrapper for the JQuery DataTables
        component within PyxleyJS. Datatables options can be passed
        through the kwargs.

        Args:
            table_id (str): html element id.
            url (str): name of the endpoint to be created.
            df (dataframe): tabular data to be rendered.
            columns (OrderedDict): columns to display. order is preserved by
                the OrderedDict.
            init_params (dict): parameters used to initialize the table.
            paging (bool): enable paging.
            searching (bool): enable searching.
            sortable (bool): enable sorting.
            classname (str): html classname for css.
            route_func (function): endpoint function. Default is None.


    """
    def __init__(self, table_id, url, df, columns={}, init_params={},
        paging=False, searching=False, sortable=False, classname="display",
        route_func=None, **kwargs):

        opts = {
            "params": init_params,
            "id": table_id,
            "url": url,
            "className": classname,
            "table_options": {
                "paging": paging,
                "searching": searching,
                "bSort": sortable
            }
        }

        for k, v in list(kwargs.items()):
            opts["table_options"][k] = v

        self.columns = columns
        self.confidence = {}
        for k, v in list(self.columns.items()):
            if "confidence" in v:
                self.confidence[k] = v["confidence"]

        if not route_func:
            def get_data():
                args = {}
                for c in init_params:
                    if request.args.get(c):
                        args[c] = request.args[c]
                    else:
                        args[c] = init_params[c]
                return jsonify(DataTable.to_json(
                        self.apply_filters(df, args),
                        self.columns,
                        confidence=self.confidence
                    ))
            route_func = get_data

        super(DataTable, self).__init__("Table", opts, route_func)

    @staticmethod
    def format_row(row, bounds, columns):
        """Formats a single row of the dataframe"""
        for c in columns:
            if c not in row:
                continue

            if "format" in columns[c]:
                row[c] = columns[c]["format"] % row[c]

            if c in bounds:
                b = bounds[c]
                row[c] = [b["min"],row[b["lower"]], row[b["upper"]], b["max"]]

        return row

    @staticmethod
    def to_json(df, columns, confidence={}):
        """Transforms dataframe to properly formatted json response"""
        records = []

        display_cols = list(columns.keys())
        if not display_cols:
            display_cols = list(df.columns)

        bounds = {}
        for c in confidence:
            bounds[c] = {
                "min": df[confidence[c]["lower"]].min(),
                "max": df[confidence[c]["upper"]].max(),
                "lower": confidence[c]["lower"],
                "upper": confidence[c]["upper"]
            }

        labels = {}
        for c in display_cols:
            if "label" in columns[c]:
                labels[c] = columns[c]["label"]
            else:
                labels[c] = c

        for i, row in df.iterrows():
            row_ = DataTable.format_row(row, bounds, columns)
            records.append({labels[c]: row_[c] for c in display_cols})

        return {
            "data": records,
            "columns": [{"data": labels[c]} for c in display_cols]
        }
