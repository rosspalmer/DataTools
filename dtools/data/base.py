import os
import pandas as pd

class data(object):

    def __init__(self):
        self.df = {}
        self.x = []
        self.y = []

    def create_tables(self):
        df = {}
        df['lr_summary'] = pd.DataFrame(columns=('test_id','n_var','n_obs','r_squared',
                                                  'adj_r_squared','f_stat','prob_f_stat'))
        df['lr_coeff']= pd.DataFrame(columns=('test_id','name','coeff','std_err','t',
                                               'p','alpha','conf_l','conf_h'))
        return df

    def xy_array(self, data_name, x_col, y_col=''):
        if isinstance(x_col, list):
            self.x = self.df[data_name][x_col].values
        else:
            self.x = self.df[data_name][[x_col]].values
        if y_col <> '':
            if isinstance(y_col, list):
                self.y = self.df[data_name][y_col].values
            else:
                self.y = self.df[data_name][[y_col]].values

    def load_csv(self, file_path, mode='single', file_search='', index=''):

        if mode == 'single':
            data_name = file_path[file_path.rfind('/')+1:-4]
            print '-- Loading %s.csv --' % data_name
            df = pd.read_csv(file_path)

        else:
            for fn in os.listdir(file_path):
                if '.csv' in fn:
                    if file_search in fn or file_search == '':
                            print '-- Loading %s --' % fn
                            df = pd.read_csv(file_path+fn)

                    if mode == 'compile':
                        df = df.append(pd.read_csv(file_path+fn), ignore_index=True)
                    elif mode == 'all':
                        if index <> '':
                            df = df.set_index(index)
                        data_name = fn[:-4]
                        self.df[data_name] = df

        if mode == 'single' or mode == 'compile':
            if mode == compile:
                data_name = file_search
            if index <> '':
                df = df.set_index(index)
            self.df[data_name] = df

    def to_csv(self, data_name, file_path, index=True):
        if data_name <> 'ALL':
            file_string = '%s%s.csv' % (file_path, data_name)
            self.df[data_name].to_csv(file_string, index=index)
        else:
            for data_name in self.df:
                file_string = '%s%s.csv' % (file_path, data_name)
                self.df[data_name].to_csv(file_string, index=index)


