import dtools as dt
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import log_loss

dh = dt.data_holder()

dh.load_csv('tt', 'examples/example_data/telstra_train.csv', y_col='fault_severity')

dh.use_ds('tt', new=True)

dh.column_filter(['event', 'severity', 'feature'])

#|---Train Models---
dh.partition(ratio=0.5)

log_mod = LogisticRegression()
log_mod.fit(dh.x, dh.y)

knn_mod = KNeighborsClassifier(50)
knn_mod.fit(dh.x, dh.y)

gbc_mod = GradientBoostingClassifier()
gbc_mod.fit(dh.x, dh.y)

rf_mod = RandomForestClassifier(1000)
rf_mod.fit(dh.x, dh.y)

#|---Predict using Test data---
dh.partition(ratio=1.0)

log_prob = log_mod.predict_proba(dh.x)

knn_prob = knn_mod.predict_proba(dh.x)

gbc_prob = gbc_mod.predict_proba(dh.x)

rf_prob = rf_mod.predict_proba(dh.x)

combo_prob = (log_prob+knn_prob+gbc_prob+rf_prob)/4

dh.format('array:class')

#|---Display LogLoss scores---
print log_loss(dh.y, log_prob)
print log_loss(dh.y, knn_prob)
print log_loss(dh.y, gbc_prob)
print log_loss(dh.y, rf_prob)
print
print log_loss(dh.y, combo_prob)