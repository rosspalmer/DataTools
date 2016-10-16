import itertools as it
import pandas as pd
from sklearn.metrics import roc_auc_score, log_loss


class CrossValidate(object):

    def __init__(self, model_object, cv_iterator):

        self.mod = model_object
        self.cv = list(cv_iterator)
        self.res = pd.DataFrame()

        self.metrics = {'classification': ['auc','logloss'],
                        'regression': ['r_squared']}

    def run(self):

        runs = self.mod.parameters
        runs['features'] = combinations(self.mod.features)
        runs = expand_grid(runs)

        model_num = 1

        for run in runs.to_dict('records'):

            if model_num % 10 == 0:
                print('-- Run (%i/%i) Complete --' %
                      (model_num, len(runs) + 1))

            cv_num = 1

            for train_index, test_index in self.cv:

                mod = self.mod.fit(run['features'], run, train_index)
                pred, act = self.mod.predict(mod, run['features'],
                                             run, test_index)

                scores = calculate_scores(pred, act)
                rows = result_rows(scores, run, model_num, cv_num)
                self.res = self.res.append(rows, ignore_index=True)

                cv_num += 1

            model_num += 1

    def feature_summary(self):

        df = self.metric_summary('feature')

        return df

    def model_summary(self):

        df = self.metric_summary('model_num')

        return df

    def metric_summary(self, groupby):

        g = self.res.groupby(groupby)
        metrics = self.metrics[self.mod.mod_type]

        df = g[metrics].mean()
        df = df.join(g[metrics].std(), rsuffix='_std')
        df = df.join(g[metrics].min(), rsuffix='_min')
        df = df.join(g[metrics].max(), rsuffix='_max')

        return df


def expand_grid(data_dict):

    rows = it.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())


def combinations(features):

    agg_list = []
    for i in range(1, len(features) + 1):
        agg_list.extend(it.combinations(features, i))

    agg_list = [list(agg) for agg in agg_list]
    return agg_list


def calculate_scores(pred, act):

    scores = {}

    scores['auc'] = roc_auc_score(act, pred)
    scores['logloss'] = log_loss(act, pred)

    return scores


def result_rows(scores, run, run_num, cv_num):

    rows = []

    for feature in run['features']:

        row = {}

        row['model_num'] = run_num
        row['cv_num'] = cv_num
        row['feature'] = feature

        param = dict(run)
        del param['features']
        row = {**row, **param}

        row = {**row, **scores}

        rows.append(row)

    return rows
