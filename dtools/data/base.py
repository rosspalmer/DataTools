import pandas as pd
import random as rn

#|Data class is used to store all data, partition data when needed,
#|and convert DataFrames into numpy arrays for statistics modules
class data_manager(object):

    #|Data class internal stores all external and internal DataFrames (df), all created models (mod),
    #|current X and Y training numpy arrays (x(y)_train) and current X and Y validation numpy arrays (x(y)_valid)
    def __init__(self):
        self.df = nest_setup()
        self.current_df = []
        self.model_id = ''
        self.x = []
        self.y = []
        self.id = []

    #|Base command to prepare data for use in statistic modules
    #|----------------------------------------------------------------------------------
    #| data_name => name of DataFrame which will be input into statistic module,
    #|              DataFrame must already be stored in "data" object
    #| x_col => string or list of strings with the names of columns to be used as "X" data
    #| y_col => string or list of strings with the names of columns to be used as "Y" data
    #| id_col =>  string or list of strings with the names of columns to be used as identifiers
    #|              for output data
    def prepare(self, type, data_name, x_col, y_col='', id_col=''):

        #|Initial Setup for DataFrame nested dictionary and determine model ID
        self.df, self.model_id = setup_df(self.df, type)

        #|Pull external data from DataFrame library
        df = self.df['external'][data_name]

        self.x, self.y = xy_array(df, x_col, y_col)
        if id_col <> '':
            self.id = id_cols(df, id_col)

        #|Create DataFrame with all data rows for test and set for later use
        self.current_df = self.test_df(x_col, y_col, id_col)

    #|Create DataFrame with all data rows for "X", "Y" and identification columns
    def test_df(self, x_col, y_col, id_col):

        #|Create "X" DataFrame
        if isinstance(x_col, list):
            df = pd.DataFrame(self.x, columns=x_col)
        else:
            df = pd.DataFrame(self.x, columns=[x_col])

        #|Create "Y" DataFrame (if required)
        if y_col <> '':
            if isinstance(y_col, list):
                df_y = pd.DataFrame(self.y, columns=y_col)
            else:
                df_y = pd.DataFrame(self.y, columns=[y_col])

            #|Join "Y" columns to "X" columns
            df = df.join(df_y)

        #|Add identification columns (if present)
        if id_col <> '':
            if isinstance(id_col, list):
                df_id = pd.DataFrame(self.id, columns=id_col)
            else:
                df_id = pd.DataFrame(self.id, columns=[id_col])
            df = df.join(df_id)

        return df

#|Create preliminary structure for nest DataFrame storage dictionaries
def nest_setup():

    df = {}
    df['external'] = {}
    df['linear'] = {}
    df['logistic'] = {}
    df['kmeans'] = {}
    df['knearest'] = {}
    return df

#|Setup DataFrames dictionary (df) with blank DataFrames if not present
#|or determine model_id as maximum value if present
def setup_df(df, type):

    if type == 'linear':
        if 'anova' in df['linear']:
            model_id = df['linear']['anova']['model_id'].max() + 1
        else:
            df['linear']['anova'] = pd.DataFrame()
            df['linear']['coeff'] = pd.DataFrame()
            df['linear']['data'] = pd.DataFrame()
            model_id = 1

    elif type == 'logistic':
        pass

    elif type == 'kmeans':
        if 'data' in df['kmeans']:
            model_id = df['kmeans']['data']['model_id'].max() + 1
        else:
            df['kmeans']['data'] = pd.DataFrame()
            df['kmeans']['clusters'] = pd.DataFrame()
            model_id = 1

    elif type == 'knearest':
        if 'data' in df['knearest']:
            model_id = df['knearest']['data']['model_id'].max() + 1
        else:
            df['knearest']['data'] = pd.DataFrame()
            model_id = 1

    return df, model_id

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

