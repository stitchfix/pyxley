
from flask import jsonify, request
import pandas as pd

class FilterFrame(object):
    """
    """
    def __init__(self,
                 dataframe,
                 columns=[],
                 to_json=None):
        self.df = dataframe.copy()
        self.columns = columns
        self.to_json = to_json

    def _apply_filters(self, filters):
        idx = pd.Series([True]*self.df.shape[0])
        for k, v in filters.items():
            if k not in self.df.columns:
                continue
            idx &= (self.df[k] == v)

        return self.df.ix[idx]

    def get(self, filters):
        return self.to_json(self._apply_filters(filters))

    def download(self, filters):
        return self._apply_filters(filters)

    def api_route(self):
        return jsonify(self.get(request.args))

    def download_route(self):
        csv = self.download(request.args).to_csv()
        response = make_response(csv)
        response.headers["Content-Disposition"] = "attachment; filename=download.csv"
        return response





