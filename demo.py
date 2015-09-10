import dtools

#|Create 'data' class object and load example CSV data
d = dtools.data()
d.from_csv('./example_csv/cereal.csv')
d.from_csv('./example_csv/cities.csv')
d.from_csv('./example_csv/loans.csv')

#|Perform Linear Regression analysis on 'cereal' example dataset
r = dtools.regression(d)
r.linear('cereal', ['Carbs','Sugars','Sodium', 'Fiber'], 'Calories')
r.linear('cereal', ['Carbs','Sugars'], 'Calories')

#|Perform Logistic regression analysis on 'loans' example dataset
r.logistic('loans', ['Income','Assets','Debts','Amount'], 'Late')

#|Perform k-Means Clustering on 'cities' example dataset
c = dtools.cluster(r.d)
c.kmeans('cities', ['% Black','% Hispanic', '% Asian', 'Median Age', 'Unemployment rate', "Per capita income(000's)"],
                3, id_col='City')
c.kmeans('cities', ['% Black','% Hispanic', '% Asian', 'Median Age', 'Unemployment rate'], 3, id_col='City')

#|Perform k-Means Nearest Neighbor classification on 'loans' example dataset
c.knearest('loans', ['Income','Assets','Debts','Amount'], 'Late', 2)

#|Dump data to CSV files on desktop
c.d.to_csv('ALL', 'ALL', '/home/ross/Desktop/')

