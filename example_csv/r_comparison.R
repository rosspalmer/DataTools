
#|Set wprking directory to example csv file
setwd('/home/ross/py/DataTools/example_csv/')

#|Load example CSV files
cereal <- read.csv('cereal.csv', stringsAsFactors = FALSE)
loans <- read.csv('loans.csv', stringsAsFactors = FALSE)

#|Run linear regression on 'cereal' file using X variables below
#|['Carbs','Sugars','Sodium', 'Fiber']
model <- lm(Calories ~ Carbs + Sugars + Sodium + Fiber, data = cereal)
summary(model)

#|Run logistic regression on 'loans' file using X variables below
#|['Income','Assets','Debts','Amount']
model <- glm(Late ~ Income + Assets + Debts + Amount, family=binomial, data = loans)
summary(model)
