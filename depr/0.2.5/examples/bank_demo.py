import dtools as dt

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier

dh = dt.data_holder()
dh.load_csv('bank', 'bank.csv', y_col='y', 
			x_col=['housing','loan','duration','pdays'])

dh.create_sub('default', col_dummy=['housing','loan'])

dh.use_ds('bank', 'default', new=True)

dh.partition(0.5)

mod = LogisticRegression()
#mod = GradientBoostingClassifier()
#mod = RandomForestClassifier()

mod.fit(dh.x, dh.y)

dh.partition(1.0)

y_hat = mod.predict_proba(dh.x)

dt.summary(dh.y.values, y_hat[:, 1], prob_hist=True, thres=0.1)
