
from flask import jsonify, request
import pandas as pd

class FilterFrame(object):
    """
    """
    def __init__(self,
                 dataframe,
                 columns=[]):
        self.df = dataframe.copy()
        self.columns = columns

    def apply_filters(self, filters):
        idx = pd.Series([True]*self.df.shape[0])
        for k, v in filters.items():
            if k not in self.df.columns:
                continue
            idx &= (self.df[k] == v)

        return self.df.ix[idx]





