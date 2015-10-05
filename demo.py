import dtools

#|Create 'data' class object and load example CSV data
m = dtools.manager('/home/ross/Desktop/hoob')
m.load_csv('./example_csv/cereal.csv')
m.load_csv('./example_csv/cities.csv')
m.load_csv('./example_csv/loans.csv')

#|Perform Linear Regression analysis on 'cereal' example dataset
m.fit_model('linear','cereal', ['Carbs','Sugars','Sodium', 'Fiber'], 'Calories')
m.fit_model('linear','cereal', ['Carbs','Sugars'], 'Calories')
m.fit_model('linear','cereal', ['Carbs','Sodium'], 'Calories')

#|Perform Logistic regression analysis on 'loans' example dataset
m.fit_model('logistic','loans', ['Income','Assets','Debts','Amount'], 'Late')
m.fit_model('logistic','loans', ['Assets','Debts'], 'Late')
#
# #|Perform k-Means Clustering on 'cities' example dataset
# m.fit_model('kmeans','cities', ['% Black','% Hispanic', '% Asian', 'Median Age', 'Unemployment rate', "Per capita income(000's)"],
#         n_cluster=3, id_col='City')
# m.fit_model('kmeans','cities', ['% Black','% Hispanic', '% Asian', 'Unemployment rate'],
#         n_cluster=3, id_col='City')
#
# #|Perform k-Means Nearest Neighbor classification on 'loans' example dataset
# m.fit_model('knearest','loans', ['Income','Assets','Debts','Amount'], 'Late', n_cluster=2)

m.display_results("ALL")

m.sql_dump()
