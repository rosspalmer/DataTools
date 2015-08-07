import os
import pandas as pd

class data(object):

    def __init__(self):
        self.df = self.create_tables()
        self.x = []
        self.y = []

    def create_tables(self):
        df = {}
        df['lr_summary'] = pd.DataFrame(columns=('test_id','n_var','n_obs','r_squared',
                                                  'adj_r_squared','f_stat','prob_f_stat'))
        df['lr_coeff']= pd.DataFrame(columns=('test_id','name','coeff','std_err','t',
                                               'p','alpha','conf_l','conf_h'))
        return df

    def xy_array(self, data_name, x_col, y_col):
        if isinstance(x_col, list):
            self.x = self.df[data_name][x_col].values
        else:
            self.x = self.df[data_name][[x_col]].values
        self.y = self.df[data_name][[y_col]].values

    def load_csv(self, data_name, file_path, file_search='', index=''):
        if file_search == '':
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame()
            for fn in os.listdir(file_path):
                if '.csv' in fn:
                    if file_search in fn:
                        print '-- Loading %s --' % fn
                        df = df.append(pd.read_csv(file_path+fn), ignore_index=True)
        if index <> '':
            df = df.set_index(index)
        self.df[data_name] = df