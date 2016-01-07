import pandas as pd

def format(mode, x, y):

    if mode == 'df':
        x = pd.DataFrame(x)
        y = pd.DataFrame(y)

    elif mode == 'array':
        x = x.values
        y = y.values

    elif mode == 'array:class':

        if isinstance(x, pd.DataFrame):
            x = x.values
        y = pd.get_dummies(y).values

    return x, y

