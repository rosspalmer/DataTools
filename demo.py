import dtools

data = dtools.data()
data.load_csv('/home/ross/data/cities.csv')
c = dtools.cluster(data)
c.kmeans('cities',['% Black','% Hispanic','% Asian','Unemployment rate'], 4)
c.kmeans('cities',['% Black','% Hispanic','% Asian','Unemployment rate'], 3)
c.kmeans('cities',['% Black','% Hispanic','% Asian','Unemployment rate'], 2)
c.d.to_csv('ALL','/home/ross/Desktop/')