import dtools

data = dtools.data()
data.load_csv('cereal', '/home/ross/data/cereal.csv')
lr = dtools.linear_regression(data)
lr.run('cereal',['Carbs','Fiber','Sugars','Sodium'],'Calories',display=True)
lr.run('cereal',['Carbs','Fiber'],'Calories',display=True)
print lr.d.tbl['lr_summary']
print lr.d.tbl['lr_coeff']
