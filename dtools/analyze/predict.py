import pandas as pd
import numpy as np
import statsmodels.api as sm

class linear_regression(object):

    #|Initialize linear reg model, load DataFrame into class, create log DataFrame,
    def __init__(self, data):
        self.d = data

    #|Determine best fit line and output data
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