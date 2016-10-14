from cv import CrossValidate

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold

import warnings
warnings.filterwarnings("ignore")

class mod_object(object):

	def __init__(self):

		self.mod_type = 'classification'
		self.features = ['age','job','education','housing','age_young']

		self.parameters = {'n_estimators':[10,50,100],
						   'age_young':[20,30,40]}

		self.df = pd.read_csv('bank-full.csv')

	def fit(self, feat, param, index):

		df = self.df.iloc[index]
		df['age_young'] = df['age'] <= param['age_young']

		x = df[feat]
		x = pd.get_dummies(x)
		y = df['subscribed']

		mod = RandomForestClassifier(n_estimators=param['n_estimators'])
		mod.fit(x.values, y.values)

		return mod

	def predict(self, mod, feat, param, index):

		df = self.df.iloc[index]
		df['age_young'] = df['age'] <= param['age_young']

		x = df[feat]
		x = pd.get_dummies(x)
		y = df['subscribed']

		pred = mod.predict_proba(x.values)[:,1]

		return pred, y.values

mobj = mod_object()
kf = KFold()
CrossValidate(mobj, kf, mobj.df)