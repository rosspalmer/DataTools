import dtools
import random as rn
from statsmodels.tools.sm_exceptions import PerfectSeparationError

m = dtools.manager('/home/ross/Desktop/hoob')
m.load_csv('/home/ross/Desktop/lendclub.csv')

SEED_NUM = 10
SEED_SIZE = 8

Y_COL = 'defaulted'
X_COL = list(m.sql.select_data('ext_lendclub').columns.values)
X_COL.remove('_id')
X_COL.remove('Unnamed: 0')
X_COL.remove(Y_COL)

error_round = False
best_models = []

for i in range(SEED_NUM):

    x_col = rn.sample(X_COL, SEED_SIZE)

    for j in range(len(x_col)-2):

        try:
            m.fit_model('logistic','lendclub',x_col,Y_COL)
        except PerfectSeparationError:
            print 'Warning: Perfect Seperation Error, End SEED'
            error_round = True
            break

        last_model_id = m.data.int_df['logistic_summary']['model_id'].max()

        coeff = m.data.int_df['logistic_coeff'][m.data.int_df['logistic_coeff']['model_id'] == last_model_id]
        coeff = coeff[coeff['name']<>'intercept']

        large_p = coeff['p'].max()
        if large_p > 0.05:
            remove_coeff = coeff[coeff['p'] == large_p]['name'].iloc[0]
            x_col.remove(remove_coeff)
        else:
            break

    if error_round:
        error_round = False
    else:
        best_models.append(coeff['model_id'].unique()[0])

m.display_results(best_models)

#m.sql_dump()

