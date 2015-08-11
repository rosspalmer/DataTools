import dtools
import pandas as pd

def cik_extract(row):
    return int(row['adsh'][:10])

d = dtools.data()
d.load_csv('/home/ross/Desktop/num.txt', sep='\t')
d.load_csv('/home/ross/Desktop/snp.csv')

d.df['num']['CIK'] = d.df['num'].apply(cik_extract, axis=1)

d.df['snp_data'] = pd.merge(d.df['num'], d.df['snp'], left_on='CIK', right_on='CIK')


col_list = []


#d.df['snp'] = d.df['snp'].sort('ddate', ascending=False)
#d.df['snp'] = d.df['snp'].drop_duplicates(['adsh','ddate']).sort('CIK')

#for value in d.df['snp']['tag'].order().unique():
#    print value