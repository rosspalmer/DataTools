import os
import pandas as pd

#|Compile CSV files from folder into single DataFrame
def compile_csv(file_path, label='', index=''):
    df = pd.DataFrame()
    for fn in os.listdir(file_path):
        if '.csv' in fn:
            if label == '' or label in fn:
                print '-- Loading %s --' % fn
                df = df.append(pd.DataFrame.from_csv(file_path+fn), ignore_index=True)
    if index <> '':
        df = df.set_index(index)
    return df