import random as rn
import pandas as pd
import sys

class data_source(object):

    def __init__(self):

        self.x = None
        self.y = None
        self.sub = {}

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

    def subset(self, sub_name, index):
        
        sub_param = self.sub[sub_name]
        col_filtered = None
        col_names = self.x.columns
        row_filt = sub_param['row_filter']

        x = self.x.loc[index]
        if self.y is not None:
            y = self.y.loc[index]
        else:
            y = None
        
        if row_filt is not None:
            final_index = []
            for col_name in row_filt.keys():
                tx = x[x[col_name]==row_filt[col_name]]
                final_index.extend(tx.index)
            final_index = list(set(final_index))                
            
            x = x.loc[final_index]
            if self.y is not None:
                y = self.y.loc[final_index]        
        
        if sub_param['col_contain'] is not None:
            if isinstance(sub_param['col_contain'], list):
                col_filtered = []
                for filt in sub_param['col_contain']:
                    col_filtered.extend([col for col in col_names \
                            if filt in col])
            elif isinstance(sub_param['col_contain'], str):
                col_filtered = [col for col in col_names \
                            if sub_param['col_contain'] in col]        

        if sub_param['col_not_contain'] is not None:
            if col_filtered is None:
                col_filtered = col_names
            if isinstance(sub_param['col_not_contain'], list):
                for filt in sub_param['col_not_contain']:
                    col_filtered.extend([col for col in col_filtered \
                            if filt not in col])
            elif isinstance(sub_param['col_not_contain'], str):
                col_filtered = [col for col in col_filtered \
                            if sub_param['col_not_contain'] not in col]
        
        if col_filtered is not None:
            x = x[col_filtered]                     

        return x, y