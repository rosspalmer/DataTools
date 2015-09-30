from excel_csv import from_csv
import pandas as pd

#|Data class is used to store all data, partition data when needed,
#|and convert DataFrames into numpy arrays for statistics modules
class data_manager(object):

    #|Data class internal stores all external and internal DataFrames (df), all created models (mod),
    #|current X and Y training numpy arrays (x(y)_train) and current X and Y validation numpy arrays (x(y)_valid)
    def __init__(self, sql):
        self.sql = sql
        self.int_df = self.load_internal_df()
        self.pred_df = {}
        self.current_df = []
        self.x = []
        self.y = []

    #|Base command to prepare data for use in statistic modules
    #|----------------------------------------------------------------------------------
    #| data_name => name of DataFrame which will be input into statistic module,
    #|              DataFrame must already be stored in "data" object
    #| x_col => string or list of strings with the names of columns to be used as "X" data
    #| y_col => string or list of strings with the names of columns to be used as "Y" data
    def prepare(self, data_name, x_col, y_col=''):

        #|Load external data set into current df variable
        ext_table_name = 'ext_%s' % data_name
        self.current_df = self.sql.select_data(ext_table_name)

        #|Create prediction table for DataFrame if not present for external dataset
        if data_name not in self.pred_df:
            self.pred_df[data_name] = pd.DataFrame(index=self.current_df.index)

        #|Convert X and Y columns into arrays and set as x and y variables
        self.x, self.y = xy_array(self.current_df, x_col, y_col)

    def load_ext_csv(self, file_path, mode, file_search, index, sep):
        df, data_name = from_csv(file_path, mode, file_search, index, sep)
        self.sql.add_new_data('ext', df, data_name)

    def load_internal_df(self):

        int_df = {}
        for table_name in self.sql.tables:
            if table_name <> 'models':
                int_df[table_name] = self.sql.select_data(table_name)
        return int_df

    def df_sql_dump(self):

        for table_name in self.int_df:
            self.sql.insert_data(self.int_df[table_name], table_name)

        if len(self.pred_df) > 0:
            for data_name in self.pred_df:
                self.sql.add_new_data('pred', self.pred_df[data_name], data_name)


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

