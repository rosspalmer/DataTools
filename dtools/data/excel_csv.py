import pandas as pd
import os

#|Load data from single or multiple CSV files into internal DataFrame within "data" object
def from_csv(data, file_path, mode, file_search, index, sep):

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
                    data.df['external'][data_name] = df

    if mode == 'single' or mode == 'compile':
        if mode == compile:
            data_name = file_search
        if index <> '':
            df = df.set_index(index)
        data.df['external'][data_name] = df

    return data

#|Output data from internal DataFrame(s) to csv
def to_csv(type, data_name, file_path, index=True):
    if data_name <> 'ALL':
        file_string = '%s%s_%s.csv' % (file_path, type, data_name)
        self.df[type][data_name].to_csv(file_string, index=index)
    else:
        for type in self.df:
            for data_name in self.df[type]:
                file_string = '%s%s_%s.csv' % (file_path, type, data_name)
                self.df[type][data_name].to_csv(file_string, index=index)