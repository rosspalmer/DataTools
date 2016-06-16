
from .formatting import format
from .source import data_source

import pandas as pd

class data_holder(object):

    def __init__(self):

        self.ds = {}
        self.x = None
        self.y = None
        self.current_ds = None
        self.current_index = []
        self.remain_index = []

    def load_csv(self, name, filepath, y_col=None, x_col=None, 
                         id_col=None, sep=','):

        df = pd.read_csv(filepath, sep=sep)
        
        if id_col is not None:
            df = df.set_index(id_col)

        if y_col is not None:
            x = df.drop(y_col, axis=1)
            y = df[y_col]
        else:
            x = df
            y = None

        if x_col is not None:
            x = x[x_col]

        self.load_ds(name, x, y)

    def load_ds(self, name, x, y=None):

        ds = data_source()
        ds.x = x
        if y is not None:
            ds.y = y
        else:
            ds.y = pd.DataFrame()
        self.ds[name] = ds

    def partition(self, ratio=1.0):

        self.x, self.y, self.remain_index = \
                self.ds[self.current_ds].partition(ratio, self.remain_index)
        self.current_index = self.x.index

    def reset_ds(self):

        self.x = self.ds[self.current_ds].x
        self.y = self.ds[self.current_ds].y

    def update_ds(self):

        self.ds[self.current_ds].x = self.x
        self.ds[self.current_ds].y = self.y

    def use_ds(self, name, new=False):

        self.current_ds = name
        if new:
            self.remain_index = self.ds[name].x.index
            self.current_index = self.ds[name].x.index

        self.x = self.ds[name].x.loc[self.remain_index]
        if self.ds[name].y is None:
            self.y = None
        else:
            self.y = self.ds[name].y.loc[self.remain_index]

    def format(self, mode):

        self.x, self.y = format(mode, self.x, self.y)
            
    def create_sub(self, sub_name, col_contain=None, col_not_contain=None,
                   row_filter=None):
                       
        sub_param = {}
        sub_param['col_contain'] = col_contain
        sub_param['col_not_contain'] = col_not_contain
        sub_param['row_filter'] = row_filter

        self.ds[self.current_ds].sub[sub_name] = sub_param

    def use_sub(self, sub_name, output_only=False, reset_index=False):

        x, y = self.ds[self.current_ds].subset(sub_name, self.current_index)
        
        if output_only:
            return x, y
        if not output_only:
            self.x = x
            self.y = y

        if reset_index:
            self.remain_index = x.index