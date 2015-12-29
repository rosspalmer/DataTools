import dtools
import pandas as pd

d = dtools.data()
d.load_csv('/home/ross/R/stocks/stocks.csv')
d.df['stocks']['vol_ma_20'] = pd.rolling_mean(d.df['stocks']['Volume'], 20)
print(d.df['stocks'])