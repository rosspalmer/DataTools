from sklearn.decomposition import PCA
import pandas as pd

def prev_cat_count(df, category_col):

    df['count'] = 1
    group = df.groupby(category_col).sum()
    group[category_col] = group.index

    return df.join(group, on=category_col, rsuffix='_R')['count_R']

def pca(df, number, name=None, verbose=0):

    mod_pca = PCA(number)
    mod_pca.fit(df)

    if verbose==1:
        print'>> Explained Variance <<'
        print mod_pca.explained_variance_
        print mod_pca.explained_variance_ratio_

    tran_pca =  mod_pca.transform(df)

    if name is None:
        name = 'pca'

    headers = []
    for i in range(number):
        headers.append('%s_%i' % (name, i))

    return pd.DataFrame(tran_pca, columns=headers, index=df.index)
