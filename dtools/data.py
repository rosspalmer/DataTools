
import pandas as pd
import random as rn
import sys

class data(object):

    def __init__(self):

        self.ds = {}
        self.eval = {}

        self.x = pd.DataFrame()
        self.y = pd.DataFrame()

    def load_csv(self, name, filepath, y_col=None, x_col=None):

        self.ds[name] = data_source()
        df = pd.read_csv(filepath)

        if y_col is not None:

            self[name].r_x = df.drop(y_col)
            self[name].r_y = df[[df]]

        else:

            self[name].r_x = df

        if x_col is not None:

            self[name].r_x = self[name].r_x[x_col]

    def connect(self, name, ratio=1.0, auto_format=None):

        if auto_format is not None:
            self.ds[name].auto = auto_format
        self.ds[name].partition(ratio)

        self.x = self[name].x
        self.y = self[name].y

    def format(self, name, mode):

        self.ds[name].format(mode)

    def create_ds(self, name, x, y=None):

        self.ds[name] = data_source()
        self.ds[name].x = x
        if y is not None:
            self.ds[name].y = y

class data_source(object):

    def __init__(self):

        self.r_x = pd.DataFrame()
        self.r_y = pd.DataFrame()
        self.x = pd.DataFrame()
        self.y = pd.DataFrame()
        self.auto = None

    def partition(self, ratio):

        if ratio < 1.0 and len(self.r_x.index) > 0:

            idx = rn.sample(self.r_x.index, int(len(self.r_x.index)*ratio))
            remain = [col for col in self.r_x.index if col not in idx]

            self.x = self.r_x.loc[idx]
            self.r_x = self.r_x.loc[remain]
            if len(self.r_y.index) > 0:
                self.y = self.r_y.loc[idx]
                self.r_y = self.r_y.loc[remain]

        elif len(self.r_x) == 0:
            sys.exit('ERROR: ZERO LENGTH REMAINING DATA')

        else:

            idx = self.r_x.index
            self.x = self.r_x.loc[idx]
            if len(self.y.index) > 0:
                self.y = self.r_y.loc[idx]

            self.r_x = pd.DataFrame()
            self.r_y = pd.DataFrame()

        if self.auto is not None:

            self.format(self.auto)

    def format(self, mode):

        if mode == 'df':
            self.x = pd.DataFrame(self.x)
            self.y = pd.DataFrame(self.y)

        elif mode == 'array':
            self.x = self.x.values
            self.y = self.y.values

