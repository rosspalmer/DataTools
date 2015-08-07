import pandas as pd
import numpy as np
import statsmodels.api as sm

class linear_regression(object):

    #|Initialize linear reg model, load DataFrame into class, create log DataFrame,
    def __init__(self, data):
        self.d = data

    #|Determine best fit line and output data
    def run(self, ext_name, x_col, y_col, display=False):

        if len(self.d.tbl['lr_summary'].index) > 0:
            test_id = self.d.tbl['lr_summary']['test_id'].max() + 1
        else:
            test_id = 1

        if isinstance(x_col, list):
            self.x = self.d.ext[ext_name][x_col].values
        else:
            self.x = self.d.ext[ext_name][[x_col]].values
        self.y = self.d.ext[ext_name][[y_col]].values

        res = sm.OLS(self.y, self.x).fit()
        summary = {'test_id':test_id, 'n_var':res.df_model, 'n_obs':res.nobs,
                   'r_squared':res.rsquared, 'adj_r_squared':res.rsquared_adj,
                   'f_stat':res.fvalue, 'prob_f_stat':res.f_pvalue}
        self.d.tbl['lr_summary'] = self.d.tbl['lr_summary'].append(summary, ignore_index=True)
        vars = []
        for i in range(len(res.tvalues)):
            var = {'test_id':test_id, 'name':x_col[i], 'coeff':res.params[i],
                   'std_err':'ERRR','t':res.tvalues[i], 'pvalues':res.pvalues[i]}
            vars.append(var)
        self.d.tbl['lr_coeff'] = self.d.tbl['lr_coeff'].append(vars, ignore_index=True)

        if display == True:
            print res.summary()