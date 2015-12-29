import dtools

m = dtools.manager('/home/ross/Desktop/hoob')
#m.load_csv('/home/ross/data/cereal.csv')
print m.data.sql.select_data('linear_summary')