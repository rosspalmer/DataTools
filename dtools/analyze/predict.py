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
        if 'anova' in self.d.df['linear']:
            test_id = self.d.df['linear']['anova']['test_id'].max() + 1
        else:
            self.d.df['linear']['anova'] = pd.DataFrame()
            self.d.df['linear']['coeff'] = pd.DataFrame()
            self.d.df['linear']['data'] = pd.DataFrame()
            test_id = 1

        #|Prepare data and fit linear regression model
        df = self.d.prepare(data_name, x_col, y_col)
        model = sm.OLS(self.d.y_train, self.d.x_train).fit()

        #|Add 'prediction' column and test_id column to test DataFrame
        df['prediction'] = model.predict(self.d.x_train)
        df['test_id'] = test_id

        #|Append current test DataFrame to compiled 'data' DataFrame
        self.d.df['linear']['data'] = self.d.df['linear']['data'].append(df, ignore_index=True)

        #|Create dictionary with individual test model summary and add to compiled 'summary' DataFrame
        anova = {'test_id':test_id, 'n_var':model.df_model, 'n_obs':model.nobs,
                   'r_squared':model.rsquared, 'adj_r_squared':model.rsquared_adj,
                   'f_stat':model.fvalue, 'prob_f_stat':model.f_pvalue}
        self.d.df['linear']['anova'] = self.d.df['linear']['anova'].append(anova, ignore_index=True)

        #|Create dictionary for each coefficent on individual test and add to compiled 'coeff' dictionary
        coeffs = []
        for i in range(len(x_col)):
            coeff = {'test_id':test_id, 'name':x_col[i], 'coeff':model.params[i],
                   'std_err':model.bse[i],'t':model.tvalues[i], 'p':model.pvalues[i],
                   'alpha':alpha,'conf_l':model.conf_int(alpha)[i][1],'conf_h':model.conf_int(alpha)[i][0]}

            #|Perform VIF calculation by performing regression of ith x_col
            #|on rest of x_col list and return R^2 value and translate to ratio
            if isinstance(x_col, list):
                ix_col = list(x_col)
                ix_col.remove(x_col[i])
                self.d.prepare(data_name, ix_col, x_col[i])
                ith_model = sm.OLS(self.d.y_train, self.d.x_train).fit()
                VIF = 1/(1-ith_model.rsquared_adj)
                coeff['VIF'] = VIF

            coeffs.append(coeff)
        self.d.df['linear']['coeff'] = self.d.df['linear']['coeff'].append(coeffs, ignore_index=True)

        #|Display individual test summary if required
        if display == True:
            print model.summary()

        #|Add to model dictionary in data class
        self.d.mod['linear'][test_id] = store_model(model, x_col, y_col)

    def logistic(self, data_name, x_col, y_col):

        df = self.d.prepare(data_name, x_col, y_col)

        model = LogisticRegression()
        model.fit(self.d.x_train, self.d.y_train)
        print model.coef_

        df['prediction'] = model.predict(self.d.x_train)
        print df.sort('prediction', ascending=False)



# |Cluster object for running and storing any cluster based analysis
class cluster(object):

    def __init__(self, data):
        self.d = data

    # |Simple KMeans clustering method for 'n_cluster' number of clusters
    def kmeans(self, data_name, x_col, n_clusters, id_col=''):

        # |Determine and set 'test_id' to the largest previous 'test_id' +1
        if 'data' in self.d.df['kmeans']:
            test_id = self.d.df['kmeans']['data']['test_id'].max() + 1
        else:
            self.d.df['kmeans']['data'] = pd.DataFrame()
            self.d.df['kmeans']['clusters'] = pd.DataFrame()
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

        self.d.df['kmeans']['data'] = self.d.df['kmeans']['data'].append(df, ignore_index=True)

        # |Create DataFrame with each cluster and the mean value for each input column
        df = pd.DataFrame()
        for i in range(n_clusters):
            clus = {'cluster':i}
            for j in range(len(x_col)):
                clus['%s_mean' % x_col[j]] = model.cluster_centers_[i][j]
            df = df.append(clus, ignore_index=True)
        df['test_id'] = test_id
        self.d.df['kmeans']['clusters'] = self.d.df['kmeans']['clusters'].append(df, ignore_index=True)

        self.d.mod['kmeans'][test_id] = store_model(model, x_col)

    def knearest(self, data_name, x_col, y_col, n_clusters, id_col=''):

        if 'data' in self.d.df['knearest']:
            test_id = self.d.df['knearest']['data']['test_id'].max() + 1
        else:
            self.d.df['knearest']['data'] = pd.DataFrame()
            test_id = 1

        df = self.d.prepare(data_name, x_col, y_col, id_col=id_col)
        df['test_id'] = test_id

        model = KNeighborsClassifier(n_clusters)
        model.fit(self.d.x_train, self.d.y_train)
        df['prediction'] = model.predict(self.d.x_train)
        self.d.df['knearest']['data'] = self.d.df['knearest']['data'].append(df, ignore_index=True)

        self.d.mod['knearest'][test_id] = store_model(model, x_col, y_col)

#|Create dictionary containing model, x column names, y column names
def store_model(model, x_col, y_col=''):
    dic = {}
    dic['model'] = model
    dic['x_col'] = x_col
    if y_col <> '':
        dic['y_col'] = y_col
    return dic

