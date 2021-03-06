import numpy as np
import pandas as pd
from matplotlib import pyplot
from sklearn.metrics import log_loss, roc_auc_score, accuracy_score
from sklearn.metrics import precision_score, recall_score, confusion_matrix
from sklearn.preprocessing import normalize

def summary(actual, predict_prob, thres=0.5, prob_hist=False):

    predict = predict_prob >= thres

    print('-----Evaluation Functions-----')
    print()
    print('AUC Score: %s' % round(roc_auc_score(actual, predict_prob), 3))
    print('LogLoss Score: %s' % round(log_loss(actual, predict_prob), 3))
    print()
    print('Accuracy: %s' % round(accuracy_score(actual, predict), 3))
    print('Precision: %s' % round(precision_score(actual, predict), 3))
    print('Recall: %s' % round(recall_score(actual, predict), 3))
    print()
    print('Predicted Proportion: %s' % round(predict.mean(), 3))
    print('Actual Proportion: %s' % round(actual.mean(), 3))
    print()
    print('-----Confusion Matrix-----')
    print()
    cm = confusion_matrix(actual, predict)
    cm_pct = []

    for i in [0,1]:
        cm_pct.append([cm[i][0]/sum(cm[i]),
                        cm[i][1]/sum(cm[i])])
    cm_pct = np.array(cm_pct)
    cm_pct = np.round(cm_pct, 3)

    print('>> Volume <<')
    print()
    print(pd.DataFrame(cm, columns=['Predict: 0','Predict: 1'],
                            index=['Actual: 0', 'Actual: 1']))
    print()
    print('>> Percentage of Actual <<')
    print()
    print(pd.DataFrame(cm_pct, columns=['Predict: 0','Predict: 1'],
                            index=['Actual: 0', 'Actual: 1']))
    print()
    
    predict_prob = pd.Series(predict_prob)

    print('-----Probability Distribution-----')
    print()
    
    df = pd.DataFrame(predict_prob[actual==0].describe([0.2,0.4,0.6,0.8]).round(3),
                        columns=['Class: 0'])

    df = df.join(predict_prob[actual==1].describe([0.2,0.4,0.6,0.8]).round(3).rename('Class: 1'))

    print(df)

    if prob_hist:

        bins = np.linspace(0, 1, 50)

        pyplot.hist(predict_prob[actual==0], bins,
            alpha=0.5, label='Class: 0', normed=True)
        pyplot.hist(predict_prob[actual==1], bins, 
                    alpha=0.5, label='Class: 1', normed=True)
        pyplot.legend(loc='upper right')
        pyplot.axvline(x=thres)
        pyplot.show()
