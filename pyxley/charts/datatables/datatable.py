from ..charts import Chart

class DataTable(Chart):
    def __init__(self, table_id, url, data_source, columns={}, init_params={},
        left_fixed=0, right_fixed=0, paging=False, searching=False,
        scroll_x=False, sortable=False, dom='<"top">rt<"bottom"lp><"clear">',
        **kwargs):

        opts = {
            "leftFixed": left_fixed,
            "rightFixed": right_fixed,
            "params": init_params,
            "id": table_id,
            "url": url,
            "table_options": {
                "paging": paging,
                "searching": searching,
                "scrollX": scroll_x,
                "bSort": sortable,
                "dom": dom
            }
        }

        for k, v in kwargs.items():
            opts["table_options"][k] = v

        self.columns = columns
        data_source.to_json = self.to_json
        super(DataTable, self).__init__("Table", opts, data_source.api_route)

    def format_row(self, row):
        for c in self.columns:
            if c not in row:
                continue

            if "format" in self.columns[c]:
                row[c] = self.columns[c]["format"] % row[c]

        return row

    def to_json(self, df):
        records = []

        display_cols = self.columns.keys()
        if not display_cols:
            display_cols = list(df.columns)

        labels = {}
        for c in display_cols:
            if "label" in self.columns[c]:
                labels[c] = self.columns[c]["label"]
            else:
                labels[c] = c

        for i, row in df.iterrows():
            row_ = self.format_row(row)
            records.append({labels[c]: row_[c] for c in display_cols})

        return {
            "data": records,
            "columns": [{"data": labels[c]} for c in display_cols]
        }
