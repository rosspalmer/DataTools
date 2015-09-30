import numpy as np
import pandas as pd
import statsmodels.api as sm

class model_manager(object):

    def __init__(self, sql):
        self.sql = sql
        self.model_object = nest_setup()
        self.model_table = self.sql.select_data('models')

    #|Create dictionary containing model, x column names, y column names
    def store_model(self, model, type, model_id, x_col, y_col):

        mod_dict = {'type':type, 'model_id':model_id}
        mod_dict['x_col'] = write_comma_delimit(x_col)
        mod_dict['y_col'] = write_comma_delimit(y_col)

        self.model_table = self.model_table.append(mod_dict, ignore_index=True)
        self.model_object[type][model_id] = model

    def next_model_id(self, type):
        model_type_table = self.model_table[self.model_table['type'] == type]
        if len(model_type_table.index) > 0:
            model_id = model_type_table['model_id'].max() + 1
        else:
            model_id = 1
        return model_id

    def add_prediction(self, data, type, model_id, data_name):

        model_table = self.model_table[self.model_table['type'] == type]
        model_table = model_table[model_table['model_id'] == model_id]

        x_col = read_comma_delimit(model_table['x_col'].iloc[0])
        y_col = read_comma_delimit(model_table['y_col'].iloc[0])

        data.prepare(data_name, x_col, y_col)
        data.x = sm.add_constant(data.x)

        model = self.model_object[type][model_id]
        pred_col_name = '%s:%s_pred_%s' % (type, str(model_id), y_col)
        prediction = pd.Series(model.predict(data.x), name= pred_col_name)
        actu_col_name = '%s:%s_actu_%s' % (type, str(model_id), y_col)
        actual = pd.Series(np.ravel(data.y), name=actu_col_name)

        if data_name not in data.pred_df:
            data.pred_df[data_name] = pd.DataFrame(index=actual.index)

        data.pred_df[data_name] = data.pred_df[data_name].join(actual)
        data.pred_df[data_name] = data.pred_df[data_name].join(prediction)
        return data


#|Create preliminary structure for nested model storage dictionaries
def nest_setup():

    df = {}
    df['linear'] = {}
    df['logistic'] = {}
    df['kmeans'] = {}
    df['knearest'] = {}
    return df

def read_comma_delimit(string):

    return string.split(',')

def write_comma_delimit(columns):

    if isinstance(columns, list):
        return ','.join(columns)
    elif len(columns) > 0:
        return columns