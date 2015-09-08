import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

class regression(object):

    def __init__(self, data):
        self.d = data

    #|Simple and multiple linear regression model
    def linear(self, data_name, x_col, y_col, alpha=0.05, display=False):

        #|Determine if linear regression DataFrames are present and if not
        #|create blank DataFrames. Also, set 'test_id'
        if 'lnr_summary' in self.d.df:
            test_id = self.d.df['lnr_summary']['test_id'].max() + 1
        else:
            self.d.df['lnr_summary'] = pd.DataFrame()
            self.d.df['lnr_coeff'] = pd.DataFrame()
            test_id = 1

        df = self.d.prepare(data_name, x_col, y_col)
        res = sm.OLS(self.d.y_train, self.d.x_train).fit()
        summary = {'test_id':test_id, 'n_var':res.df_model, 'n_obs':res.nobs,
                   'r_squared':res.rsquared, 'adj_r_squared':res.rsquared_adj,
                   'f_stat':res.fvalue, 'prob_f_stat':res.f_pvalue}
        self.d.df['lnr_summary'] = self.d.df['lnr_summary'].append(summary, ignore_index=True)

        coeffs = []
        for i in range(len(res.tvalues)):
            coeff = {'test_id':test_id, 'name':x_col[i], 'coeff':res.params[i],
                   'std_err':res.bse[i],'t':res.tvalues[i], 'p':res.pvalues[i],
                   'alpha':alpha,'conf_l':res.conf_int(alpha)[i][1],'conf_h':res.conf_int(alpha)[i][0]}
            coeffs.append(coeff)
        self.d.df['lnr_coeff'] = self.d.df['lnr_coeff'].append(coeffs, ignore_index=True)

        if display == True:
            print res.summary()

# |Cluster object for running and storing any cluster based analysis
class cluster(object):

    def __init__(self, data):
        self.d = data

    # |Simple KMeans clustering method for 'n_cluster' number of clusters
    def kmeans(self, data_name, x_col, n_clusters, id_col=''):

        # |Determine and set 'test_id' to the largest previous 'test_id' +1
        if 'km_data' in self.d.df:
            test_id = self.d.df['km_data']['test_id'].max() + 1
        else:
            self.d.df['km_data'] = pd.DataFrame()
            self.d.df['km_clusters'] = pd.DataFrame()
            test_id = 1

        # |Prepare data by creating array and DataFrame using columns in 'x_col'
        df = self.d.prepare(data_name, x_col, id_col=id_col)

        #|Add test ID number and identifier columns
        df['test_id'] = test_id

        # |Create model, fit data, and return prediction of cluster for each row
        model = KMeans(n_clusters)
        df['cluster'] = model.fit_predict(self.d.x_train)

        # |Add distance to each cluster for each row to summary data
        headers = []
        for i in range(n_clusters):
            headers.append('dist_%s' % str(i))
        dist = pd.DataFrame(model.transform(self.d.x_train), columns=headers)
        df = df.join(dist)

        self.d.df['km_data'] = self.d.df['km_data'].append(df, ignore_index=True)

        # |Create DataFrame with each cluster and the mean value for each input column
        df = pd.DataFrame()
        for i in range(n_clusters):
            clus = {'cluster':i}
            for j in range(len(x_col)):
                clus['%s_mean' % x_col[j]] = model.cluster_centers_[i][j]
            df = df.append(clus, ignore_index=True)
        df['test_id'] = test_id
        self.d.df['km_clusters'] = self.d.df['km_clusters'].append(df, ignore_index=True)

        model_id = 'kmeans_%s' % str(test_id)
        self.d.mod[model_id] = model

    def knearest(self, data_name, x_col, y_col, n_clusters, id_col=''):

        if 'kn_data' in self.d.df:
            test_id = self.d.df['kn_data']['test_id'].max() + 1
        else:
            self.d.df['kn_data'] = pd.DataFrame()
            test_id = 1

        df = self.d.prepare(data_name, x_col, y_col, id_col=id_col)
        df['test_id'] = test_id

        model = KNeighborsClassifier(n_clusters)
        model.fit(self.d.x_train, self.d.y_train)
        df['prediction'] = model.predict(self.d.x_train)
        self.d.df['kn_data'] = self.d.df['kn_data'].append(df, ignore_index=True)

        model_id = 'knearest_%s' % str(test_id)
        self.d.mod[model_id] = model

