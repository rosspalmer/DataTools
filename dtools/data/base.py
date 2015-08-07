import os
import pandas as pd

class data(object):

    def __init__(self):
        self.tbl = self.create_tables()
        self.ext = {}

    def create_tables(self):
        tbl = {}
        tbl['lr_summary'] = pd.DataFrame(columns=('test_id','n_var','n_obs','r_squared',
                                                  'adj_r_squared','f_stat','prob_f_stat'))
        tbl['lr_coeff']= pd.DataFrame(columns=('test_id','name','coeff','std_err','t',
                                               'pvalue','conf_95l','conf_95h'))
        return tbl

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
        self.ext[data_name] = df