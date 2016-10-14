# DataTools

_Note: Currently going under complete re-development, please come back later_

_Last Updated: 10/14/16_

DataTools is a Python module which provides tools to aid in predictive modeling and machine learning development. DataTools is designed to be generic enough to be applied to any model but contains a specific set of tools I find useful in my role as a data scientist. The purpose of DataTools is to save time and effort writing code to perform the complex tasks below but is not meant to be a standalone modeling package.

## Toolset (in development)

- Model Evaluation
  - Classification
  - Regression(like)
  - Automated parameter selection
- Feature Evaluation
  - Automated feature selection
  - Feature variance visualization
  - Interaction 
- Feature Creation
  - Time-based transaction data conversion
- Data Manipulation
  - Fill missing values

## `CrossValidate` - Automated feature and parameter selection

DataTools provides a `CrossValidate` function which evaluates a user's model over a range of different features and parameters and provides an easy to read results. Currently this is accomplished through a brute grid search but more intelligent search methods will be added later.

The `CrossValidate` function can be used on **any** predictive model but the model must be passed with a "wrapper object" which contains the methods listed in the example wrapper below.

    class wrapper_template(object):
    
        def __init__(self):
        
            #|Set to either 'classification' or 'regression' based
            #|on model type (will determine evaluation functions)
            self.mod_type = 'classification' 
            
            self.features = ['var_a','var_b','var_c']
            
            self.parameters = {'A':[1,5,10], 'B':['dog','cat']}
            
        def fit(self, feat, param, index):
        
            return model
            
        def predict(self, feat, param, index):
        
            return prediction, actual
    
