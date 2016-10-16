from cross_validate import CrossValidate

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold

import warnings
warnings.filterwarnings("ignore")

class mod_object(object):

    def __init__(self):

        self.mod_type = 'classification'
        self.features = ['job','education','housing','age_young',
                         'campaign','pdays']

        self.parameters = {'age_young':[20,30,40],'C':[0.1,0.5,1,5]}

        self.df = pd.read_csv('bank-full.csv')

    def fit(self, feat, param, index):

        df = self.df.iloc[index]
        df['age_young'] = df['age'] <= param['age_young']

        x = df[feat]
        x = pd.get_dummies(x, drop_first=True)
        y = df['subscribed']

        mod = LogisticRegression(C=param['C'], solver='sag')
        mod.fit(x.values, y.values)

        return mod

    def predict(self, mod, feat, param, index):

        df = self.df.iloc[index]
        df['age_young'] = df['age'] <= param['age_young']

        x = df[feat]
        x = pd.get_dummies(x, drop_first=True)
        y = df['subscribed']

        pred = mod.predict_proba(x.values)[:, 1]

        return pred, y.values


mobj = mod_object()
kf = KFold(n_splits=5, shuffle=True).split(mobj.df)
cv = CrossValidate(mobj, kf)

cv.run()

print(cv.feature_summary())
print(cv.model_summary().sort_values('auc', ascending=False))

cv.res.to_csv('test.csv')