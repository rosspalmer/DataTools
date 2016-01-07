
from formatting import format
from source import data_source

import pandas as pd

class data_holder(object):

    def __init__(self):

        self.ds = {}

        self.x = pd.DataFrame()
        self.y = pd.DataFrame()
        self.current_ds = None
        self.remain_index = []

    def load_csv(self, name, filepath, y_col=None, x_col=None, sep=','):

        df = pd.read_csv(filepath, sep=sep)

        if y_col is not None:
            x = df.drop(y_col, axis=1)
            y = df[y_col]

        else:
            x = df
            y = None

        if x_col is not None:
            x = x[x_col]

        self.load_ds(name, x, y)

    def partition(self, ratio=1.0, remove=True):

        if remove:
            self.remain_index = self.ds[self.current_ds].partition(ratio, self.remain_index)
        elif remove is False:
            self.ds[self.current_ds].partition(ratio, self.remain_index)

        self.x = self.ds[self.current_ds].x
        self.y = self.ds[self.current_ds].y

    def use_ds(self, name, new=False):

        self.current_ds = name
        if new:
            self.remain_index = self.ds[name].f_x.index
        self.partition(remove=False)

    def format(self, mode):

        self.x, self.y = format(mode, self.x, self.y)

    def column_filter(self, contains=None, non_contains=None):

        self.ds[self.current_ds].column_filter(contains, non_contains)
        self.x = self.ds[self.current_ds].x

    def load_ds(self, name, x, y=None):

        self.ds[name] = data_source()
        self.ds[name].f_x = x
        if y is not None:
            self.ds[name].f_y = y
        else:
            self.ds[name].f_y = pd.DataFrame()

