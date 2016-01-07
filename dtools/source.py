import random as rn
import pandas as pd
import sys

class data_source(object):

    def __init__(self):

        self.f_x = pd.DataFrame()
        self.f_y = pd.DataFrame()
        self.x = pd.DataFrame()
        self.y = pd.DataFrame()

    def partition(self, ratio, remain_index):

        if not len(remain_index) > 0:
            sys.exit('ERROR: ZERO LENGTH REMAINING DATA')

        else:

            if ratio < 1.0:
                idx = rn.sample(self.f_x.index, int(len(remain_index)*ratio))
                remain_index = [id for id in remain_index if id not in idx]

            else:
                idx = remain_index
                remain_index = []

        self.x = self.f_x.loc[idx]
        if len(self.f_y.index) > 0:
            self.y = self.f_y.loc[idx]

        return remain_index

    def column_filter(self, contain, not_contain):

        col_names = self.f_x.columns

        if contain is not None:
            if isinstance(contain, list):
                col_filtered = []
                for filt in contain:
                    col_filtered.extend([col for col in col_names if filt in col])
            elif isinstance(contain, str):
                col_filtered = [col for col in col_names if contain in col]

        if not_contain is not None:
            if isinstance(not_contain, list):
                for filt in not_contain:
                    col_filtered.extend([col for col in col_filtered if filt not in col])
            elif isinstance(not_contain, str):
                col_filtered = [col for col in col_filtered if not_contain not in col]

        self.x = self.f_x[col_filtered]

