from ..data import data_manager, from_csv
from ..analyze import linear, logistic, kmeans, knearest

class manager(object):

    def __init__(self):
        self.data = data_manager()
        self.mod = nest_setup()

    #|Load CSV file(s) into 'external' df DataFrame library
    def load_csv(self, file_path, mode='single', file_search='', index='', sep=','):
        self.data = from_csv(self.data, file_path, mode, file_search, index, sep)

    #|Initial command to fit and run model
    def fit_model(self, type, data_name, x_col, y_col='', id_col='',
                  alpha=0.05, n_cluster=2):

        #|Prepare data for model
        self.data.prepare(type, data_name, x_col, y_col, id_col)

        #|Fit model and return result data
        if type == 'linear':
            self.data, model = linear(self.data, x_col, alpha)
        elif type == 'logistic':
            self.data, model = logistic(self.data)
        elif type == 'kmeans':
            self.data, model = kmeans(self.data, x_col, n_cluster)
        elif type == 'knearest':
            self.data, model = knearest(self.data, n_cluster)

        #|Store model, data_name, and columns run
        self.mod[type][self.data.model_id] = store_model(model, data_name, x_col, y_col, id_col)

#|Create preliminary structure for nested model storage dictionaries
def nest_setup():

    df = {}
    df['linear'] = {}
    df['logistic'] = {}
    df['kmeans'] = {}
    df['knearest'] = {}
    return df

#|Create dictionary containing model, x column names, y column names
def store_model(model, data_name, x_col, y_col, id_col):
    dic = {}
    dic['model'] = model
    dic['data_name'] = data_name
    dic['x_col'] = x_col
    if y_col <> '':
        dic['y_col'] = y_col
    if id_col <> '':
        dic['id_col'] = id_col
    return dic