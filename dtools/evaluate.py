import pandas as pd

def threshold_analysis(model, cv_iterator, feat, param):

    res = pd.DataFrame()

    cv_num = 1

    for train_index, test_index in cv_iterator:

        mod = model.fit(feat, param, train_index)
        pred, act = model.predict(mod, feat,
                                  param, test_index)

        data = {'decision':pred, 'actual':act}
        df = pd.DataFrame(data)
        df['cv_num'] = cv_num

        res = res.append(df)

        cv_num += 1


