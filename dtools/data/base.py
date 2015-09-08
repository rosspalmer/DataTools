import os
import pandas as pd
import random as rn

#|Data class is used to store all data, partition data when needed,
#|and convert DataFrames into numpy arrays for statistics modules
class data(object):

    #|Data class internal stores all external and internal DataFrames (df), all created models (mod),
    #|current X and Y training numpy arrays (x(y)_train) and current X and Y validation numpy arrays (x(y)_valid)
    def __init__(self):
        self.df = {}
        self.mod = {}
        self.x_train = []
        self.y_train = []
        self.id_train = []
        self.x_valid = []
        self.y_valid = []
        self.id_valid = []

    #|Base command to prepare data for use in statistic modules
    #|----------------------------------------------------------------------------------
    #| data_name => name of DataFrame which will be input into statistic module,
    #|              DataFrame must already be stored in "data" object
    #| x_col => string or list of strings with the names of columns to be used as "X" data
    #| y_col => string or list of strings with the names of columns to be used as "Y" data
    #| y_partition => define "Y" value which is considered a "success" when partitioning data
    #|                  If set to "None" then the data will NOT be partitioned
    #| train_size => count size of the training set, must be interger and remaining count
    #|                 will be used a validation set (NOT FUNCTIONAL YET)
    #| train_ratio => set ratio of "success" Y values to "non-success" Y values in training set
    #| id_col =>  string or list of strings with the names of columns to be used as identifiers
    #|              for output data
    def prepare(self, data_name, x_col, y_col='', y_success=None,
                train_size='all', train_ratio=0.5, id_col=''):

        #|Pull external data from DataFrame library
        df = self.df[data_name]

        #|Create X and Y numpy arrays where all data is to be used for training set
        if train_size == 'all':
            self.x_train, self.y_train = xy_array(df, x_col, y_col)
            if id_col <> '':
                self.id_train = id_cols(df, id_col)

        #|Create X and Y numpy arrays where data will be partitioned
        else:

            df['random'] = rn.randint(1,len(df.index)*2)
            df = df.sort('random')

            if y_success == None:
                self.x_train, self.y_train = xy_array(df[:train_size-1], x_col, y_col)
                self.x_valid, self.y_valid = xy_array(df[train_size:], x_col, y_col)
                if id_col <> '':
                    self.id_train = id_cols(df[:train_size-1], id_col)
                    self.id_valid = id_cols(df[train_size:], id_col)

            else:
                win = df[df[y_col] == y_success]
                lose = df[df[y_col] <> y_success]
                self.x_train, self.y_train = xy_array(win[:train_size-1]\
                                                           .append(lose[:train_size-1], ignore_index=True))
                self.x_valid, self.y_valid = xy_array(win[train_size:]\
                                                           .append(lose[train_size:], ignore_index=True))

                if id_col <> '':
                    self.id_train = id_cols(win[:train_size-1].append(lose[:train_size-1], ignore_index=True))
                    self.id_valid = id_cols(win[train_size:].append(lose[train_size:], ignore_index=True))

        return self.test_df(x_col, y_col, id_col)

    #|Create DataFrame with all data rows for "X", "Y" and identification columns
    def test_df(self, x_col, y_col, id_col):

        #|Create "X" DataFrame
        if isinstance(x_col, list):
            df = pd.DataFrame(self.x_train, columns=x_col)
        else:
            df = pd.DataFrame(self.x_train, columns=[x_col])

        #|Create "Y" DataFrame (if required)
        if y_col <> '':
            if isinstance(y_col, list):
                df_y = pd.DataFrame(self.y_train, columns=y_col)
            else:
                df_y = pd.DataFrame(self.y_train, columns=[y_col])

            #|Join "Y" columns to "X" columns
            df = df.join(df_y)

        #|Add identification columns (if present)
        if id_col <> '':
            if isinstance(id_col, list):
                df_id = pd.DataFrame(self.id_train, columns=id_col)
            else:
                df_id = pd.DataFrame(self.id_train, columns=[id_col])
            df = df.join(df_id)

        return df

    #|Load data from single or multiple CSV files into internal DataFrame within "data" object
    def from_csv(self, file_path, mode='single', file_search='', index='', sep=','):

        if mode == 'single':
            data_name = file_path[file_path.rfind('/')+1:-4]
            print '-- Loading %s.csv --' % data_name
            df = pd.read_csv(file_path, sep=sep)

        else:
            for fn in os.listdir(file_path):
                if '.csv' in fn:
                    if file_search in fn or file_search == '':
                            print '-- Loading %s --' % fn
                            df = pd.read_csv(file_path+fn, sep=sep)

                    if mode == 'compile':
                        df = df.append(pd.read_csv(file_path+fn, sep=sep), ignore_index=True)
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

    #|Output data from internal DataFrame(s) to csv
    def to_csv(self, data_name, file_path, index=True):
        if data_name <> 'ALL':
            file_string = '%s%s.csv' % (file_path, data_name)
            self.df[data_name].to_csv(file_string, index=index)
        else:
            for data_name in self.df:
                file_string = '%s%s.csv' % (file_path, data_name)
                self.df[data_name].to_csv(file_string, index=index)

#|Convert DataFrame X and Y columns into numpy arrays
def xy_array(df, x_col, y_col):

    if isinstance(x_col, list):
        x = df[x_col].values
    else:
        x = df[[x_col]].values
    if y_col <> '':
        if isinstance(y_col, list):
            y = df[y_col].values
        else:
            y = df[[y_col]].values
    else:
        y = ''

    return x, y

#|Return DataFrame or Series of identification columns
def id_cols(df, id_col):

    if isinstance(id_col, list):
        id = df[id_col]
    else:
        id = df[[id_col]]
    return id

