from ..charts import Chart
from flask import jsonify, request

class DataTable(Chart):
    def __init__(self, table_id, url, data_source, columns={}, init_params={},
        paging=False, searching=False, sortable=False, classname="display", **kwargs):

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

        for k, v in kwargs.items():
            opts["table_options"][k] = v

        self.columns = columns
        self.confidence = {}
        for k, v in self.columns.items():
            if "confidence" in v:
                self.confidence[k] = v["confidence"]

        def get_data():
            return jsonify(self.to_json(
                    data_source.apply_filters(request.args)
                ))

        super(DataTable, self).__init__("Table", opts, get_data)

    def format_row(self, row, bounds):
        for c in self.columns:
            if c not in row:
                continue

            if "format" in self.columns[c]:
                row[c] = self.columns[c]["format"] % row[c]

            if c in bounds:
                b = bounds[c]
                row[c] = [b["min"],row[b["lower"]], row[b["upper"]], b["max"]]

        return row

    def to_json(self, df):
        records = []

        display_cols = self.columns.keys()
        if not display_cols:
            display_cols = list(df.columns)

        bounds = {}
        for c in self.confidence:
            bounds[c] = {
                "min": df[self.confidence[c]["lower"]].min(),
                "max": df[self.confidence[c]["upper"]].max(),
                "lower": self.confidence[c]["lower"],
                "upper": self.confidence[c]["upper"]
            }

        labels = {}
        for c in display_cols:
            if "label" in self.columns[c]:
                labels[c] = self.columns[c]["label"]
            else:
                labels[c] = c

        for i, row in df.iterrows():
            row_ = self.format_row(row, bounds)
            records.append({labels[c]: row_[c] for c in display_cols})

        return {
            "data": records,
            "columns": [{"data": labels[c]} for c in display_cols]
        }
