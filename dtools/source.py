import random as rn
import pandas as pd
import sys

class data_source(object):

    def __init__(self):

        self.x = None
        self.y = None

    def partition(self, ratio, remain_index):

        if not len(remain_index) > 0:
            sys.exit('ERROR: ZERO LENGTH REMAINING DATA')

        else:

            if ratio < 1.0:
                idx = rn.sample(remain_index, int(len(remain_index)*ratio))
                remain_index = [id for id in remain_index if id not in idx]

            else:
                idx = remain_index
                remain_index = []

        x = self.x.loc[idx]
        if self.y is not None:
            y = self.y.loc[idx]
        else:
            y = None

        return x, y, remain_index

    def subset(self, params):
        
        x = self.x
        y = self.y

        if params['col_filter'] is not None:
            x = x[params]

        if params['col_dummy'] is not None:
            x = pd.get_dummies(x, columns=params['col_dummy'], drop_first=True)

        return x, y
