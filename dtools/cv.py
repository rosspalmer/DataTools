import itertools as it
import pandas as pd
from sklearn.metrics import roc_auc_score

def CrossValidate(model_object, cv_iterator, data):

	runs = model_object.parameters
	runs['features'] = combinations(model_object.features)
	runs = expand_grid(runs)
	runs = runs.to_dict('records')

	res = []

	for run in runs:

		cv_results = []

		for train_index, test_index in cv_iterator.split(data.values):

			mod = model_object.fit(run['features'], run, train_index)
			pred, act = model_object.predict(mod, run['features'], 
											 run, test_index)

			cv_results.append(roc_auc_score(act, pred))

		print(run)
		print(cv_results)
		print()

def expand_grid(data_dict):
	rows = it.product(*data_dict.values())
	return pd.DataFrame.from_records(rows, columns=data_dict.keys())

def combinations(features):

    agg_list = []
    for i in range(1, len(features)+1):
        agg_list.extend(it.combinations(features, i))
        
    agg_list = [list(agg) for agg in agg_list]
    return agg_list
