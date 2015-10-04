import pandas as pd
import statsmodels.api as sm
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier

#|Simple and multiple linear regression model
def linear(data, model_id, x_col, alpha):

    #|Fit linear regression model
    data.x = sm.add_constant(data.x)
    model = sm.OLS(data.y, data.x).fit()

    #|Create dictionary with individual test model summary and add to compiled 'summary' DataFrame
    summary = {'model_id':model_id, 'n_var':model.df_model, 'n_obs':model.nobs,
               'r_squared':model.rsquared, 'adj_r_squared':model.rsquared_adj,
               'f_stat':model.fvalue, 'prob_f_stat':model.f_pvalue}
    data.int_df['linear_summary'] = data.int_df['linear_summary'].append(summary, ignore_index=True)

    #|Build coefficients table and add to data object
    coeffs = sm_regression_coeffs('linear', model, model_id, x_col, alpha)
    data.int_df['linear_coeff'] = data.int_df['linear_coeff'].append(coeffs, ignore_index=True)

    return data, model

def logistic(data, model_id, x_col, alpha):

    data.x = sm.add_constant(data.x)
    model = sm.GLM(data.y, data.x, family=sm.families.Binomial(sm.families.links.logit)).fit()

    summary = {'model_id':model_id, 'n_var':model.df_model, 'n_obs':model.nobs,
               'log_likely':model.llf, 'aic':model.aic,
               'p_chi2':model.pearson_chi2, 'deviance':model.deviance}
    data.int_df['logistic_summary'] = data.int_df['logistic_summary'].append(summary, ignore_index=True)

    #|Build coefficients table and add to DataFrame dictionary
    coeffs = sm_regression_coeffs('logistic', model, model_id, x_col, alpha)
    data.int_df['logistic_coeff'] = data.int_df['logistic_coeff'].append(coeffs, ignore_index=True)

    return data, model

# |Simple KMeans clustering method for 'n_cluster' number of clusters
def kmeans(data, model_id, x_col, n_clusters):

    #|Add test ID number and identifier columns
    data.current_df['model_id'] = model_id

    # |Create model, fit data, and return prediction of cluster for each row
    model = KMeans(n_clusters)
    data.current_df['predicted_cluster'] = model.fit_predict(data.x)

    # |Add distance to each cluster for each row to summary data
    headers = []
    for i in range(n_clusters):
        headers.append('dist_%s' % str(i))
    dist = pd.DataFrame(model.transform(data.x), columns=headers)
    data.current_df = data.current_df.join(dist)

    data.df['kmeans']['data'] = data.df['kmeans']['data'].append(data.current_df, ignore_index=True)

    # |Create DataFrame with each cluster and the mean value for each input column
    df = pd.DataFrame()
    for i in range(n_clusters):
        clus = {'cluster':i}
        for j in range(len(x_col)):
            clus['%s_mean' % x_col[j]] = model.cluster_centers_[i][j]
        df = df.append(clus, ignore_index=True)
    df['model_id'] = model_id
    data.df['kmeans']['clusters'] = data.df['kmeans']['clusters'].append(df, ignore_index=True)

    return data, model

def knearest(data, model_id, n_clusters):

    data.current_df['model_id'] = model_id

    model = KNeighborsClassifier(n_clusters)
    model.fit(data.x, data.y)
    data.current_df['prediction'] = model.predict(data.x)
    data.df['knearest']['data'] = data.df['knearest']['data'].append(data.current_df, ignore_index=True)

    return data, model

def sm_regression_coeffs(type, model, model_id, x_col, alpha):
    coeffs = []
    for i in range(len(x_col)):
        if i > 0:
            name = x_col[i-1]
        else:
            name = 'intercept'
        coeff = {'model_id':model_id, 'name':name, 'coeff':model.params[i],
                 'std_err':model.bse[i], 't':model.tvalues[i], 'p':model.pvalues[i],
                 'alpha':alpha, 'conf_l':model.conf_int(alpha)[i][1], 'conf_h':model.conf_int(alpha)[i][0]}
        if type == 'logistic':
            coeff['z'] = coeff.pop('t')
        coeffs.append(coeff)
    return coeffs