from project import project
from view import display_summary
from ..data import data_manager, to_csv, sql_manager, model_manager
from ..analyze import linear, logistic, kmeans, knearest

class manager(object):

    def __init__(self, project_folder):
        self.proj = project(project_folder)
        self.sql = sql_manager(self.proj)
        self.data = data_manager(self.sql)
        self.model = model_manager(self.sql)

    #|Load CSV file(s) into 'external' df DataFrame library
    def load_csv(self, file_path, mode='single', file_search='', index='', sep=','):
        self.data.load_ext_csv(file_path, mode, file_search, index, sep)

    #|Output CSV file(s) to location. Note: Set data_name to 'ALL' to output all data
    def to_csv(self, type, data_name, file_path, index=False):
        to_csv(self.data, type, data_name, file_path, index)

    #|Initial command to fit and run model
    def fit_model(self, type, data_name, x_col, y_col='', alpha=0.05, n_cluster=2):

        #|Determine model_id number by checking previous models for type
        model_id = self.model.next_model_id()

        #|Prepare data for model
        self.data.prepare(data_name, x_col, y_col, 'train')

        #|Fit model and return result data
        if type == 'linear':
            self.data, model = linear(self.data, model_id, x_col, alpha)
        elif type == 'logistic':
            self.data, model = logistic(self.data, model_id, x_col, alpha)
        elif type == 'kmeans':
            self.data, model = kmeans(self.data, model_id, x_col, n_cluster)
        elif type == 'knearest':
            self.data, model = knearest(self.data, model_id, n_cluster)

        #|Store model object and associated data for future runs
        self.model.store_model(model, type, model_id, x_col, y_col)

        #|Add prediction to 'pred' DataFrame in data object
        self.data = self.model.add_prediction(self.data, model_id, data_name, 'train')

    #|Run prediction on test partition for dataset and model_id
    def predict(self, model_id, data_name):

        self.model.add_prediction(self.data, model_id, data_name, 'test')

    #|Return data as DataFrame
    def output_df(self, type, table_name, predict=False):

        if type == 'ext':
            return self.data.output_ext(table_name, predict)

    #|Insert internal DataFrames into SQL database
    def sql_dump(self):

        self.data.df_sql_dump()

        self.sql.insert_data(self.model.model_table, 'models')

    #|Display model results
    def display_results(self, model_list):

        display_summary(self.data, self.model, model_list)

    #|Set partition to dataset
    def partition_data(self, data_name, ratio='', seed=''):

        self.data.set_partition(data_name, ratio, seed)