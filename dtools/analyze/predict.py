import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.cluster import KMeans

class linear_regression(object):

    def __init__(self, data):
        self.d = data

    def run(self, data_name, x_col, y_col, alpha=0.05, display=False):

        if len(self.d.df['lr_summary'].index) > 0:
            test_id = self.d.df['lr_summary']['test_id'].max() + 1
        else:
            test_id = 1

        self.d.xy_array(data_name, x_col, y_col)

        res = sm.OLS(self.d.y, self.d.x).fit()
        summary = {'test_id':test_id, 'n_var':res.df_model, 'n_obs':res.nobs,
                   'r_squared':res.rsquared, 'adj_r_squared':res.rsquared_adj,
                   'f_stat':res.fvalue, 'prob_f_stat':res.f_pvalue}
        self.d.df['lr_summary'] = self.d.df['lr_summary'].append(summary, ignore_index=True)

        vars = []
        for i in range(len(res.tvalues)):
            var = {'test_id':test_id, 'name':x_col[i], 'coeff':res.params[i],
                   'std_err':res.bse[i],'t':res.tvalues[i], 'p':res.pvalues[i],
                   'alpha':alpha,'conf_l':res.conf_int(alpha)[i][1],'conf_h':res.conf_int(alpha)[i][0]}
            vars.append(var)
        self.d.df['lr_coeff'] = self.d.df['lr_coeff'].append(vars, ignore_index=True)

        if display == True:
            print res.summary()

class cluster(object):

    def __init__(self, data):
        self.d = data

    def kmeans(self, data_name, x_col, n_clusters, y_col=''):

        self.d.xy_array(data_name, x_col, y_col)
        model = KMeans(n_clusters)
        df = pd.DataFrame(self.d.df[data_name])

        if y_col == '':
            df['cluster'] = model.fit_predict(self.d.x)
        else:
            df['cluster'] = model.fit_predict(self.d.x, self.d.y)

        headers = []
        for i in range(n_clusters):
            headers.append('dist_%s' % str(i))
        dist = pd.DataFrame(model.transform(self.d.x), columns=headers)
        df = df.join(dist)

        max = 0
        for df_name in self.d.df:
            if 'kc_data_' in df_name:
                num = int(df_name[df_name.rfind('_')+1:])
                if num >= max:
                    max = num + 1
        self.d.df['kc_data_%s' % str(max)] = df

        print(model.cluster_centers_)

        summary = pd.DataFrame()
        for i in range(n_clusters):
            clus = {'cluster':i}
            for j in range(len(x_col)):
                clus['%s_mean' % x_col[j]] = model.cluster_centers_[i][j]
            summary = summary.append(clus, ignore_index=True)
        self.d.df['kc_summary_%s' % max] = summary


