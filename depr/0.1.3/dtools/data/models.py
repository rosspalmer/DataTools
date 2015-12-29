import numpy as np
import pandas as pd
import statsmodels.api as sm

class model_manager(object):

    #|Initialize with SQL manager, model object dictionary and model info DataFrame
    def __init__(self, sql):
        self.sql = sql
        self.model_object = {}
        self.model_table = self.sql.select_data('models')

    #|Create individual dictionary containing model, x column names, y column names
    def store_model(self, model, type, model_id, x_col, y_col):

        #|Initialize dictionary and convert x and y lists to comma delimited strings
        mod_dict = {'type':type, 'model_id':model_id}
        mod_dict['x_col'] = write_comma_delimit(x_col)
        mod_dict['y_col'] = write_comma_delimit(y_col)

        #|Add indivdual model info to model table and store model object
        self.model_table = self.model_table.append(mod_dict, ignore_index=True)
        self.model_object[model_id] = model

    #|Determine next model id by checking max 'model_id' on model info DataFrame
    def next_model_id(self):
        if len(self.model_table.index) > 0:
            model_id = self.model_table['model_id'].max() + 1
        else:
            model_id = 1
        return model_id

    #|Use model to add prediction column to dataset
    def add_prediction(self, data, model_id, data_name, mode):

        #|Load model info for 'model_id'
        model_table = self.model_table[self.model_table['model_id'] == model_id]
        type = model_table['type'].values[0]

        #|Convert comma delimited x and y values into list
        x_col = read_comma_delimit(model_table['x_col'].iloc[0])
        y_col = read_comma_delimit(model_table['y_col'].iloc[0])[0]

        #|Prepare data for model and add constant for regression models
        data.prepare(data_name, x_col, y_col, mode)
        data.x = sm.add_constant(data.x)

        #|Run prediction and create prediction column header names
        model = self.model_object[model_id]
        pred_col_name = '%s:%s_%s' % (mode, str(model_id), y_col)
        prediction = pd.Series(model.predict(data.x), name= pred_col_name, index=data.current_df.index)

        #|Add actual and prediction columns to dataset specific prediction DataFrame
        data.pred_df[data_name] = data.pred_df[data_name].join(prediction, how='outer')
        return data


#|Convert comma delimited string to list
def read_comma_delimit(string):

    return string.split(',')

#|Convert lists to comma delimited string
def write_comma_delimit(columns):

    if isinstance(columns, list):
        return ','.join(columns)
    elif len(columns) > 0:
        return columns