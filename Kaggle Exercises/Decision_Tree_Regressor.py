#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor


# In[2]:


home_data = pd.read_csv('train_home_data.csv')


# In[3]:


home_data.head(5)


# In[16]:


print('rows in dataset: ',len(home_data), 'columns in dataset: ',len(home_data.columns))


# # Creation of target object

# In[17]:


y = home_data.SalePrice


# # Creating a list of features
# ## Out of the 81 columns, only the selected 7 features (columns) will be used

# In[18]:


features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']


# # Creating a subset of data using the features

# In[19]:


X = home_data[features]


# In[27]:


print('rows in X: ',len(X),'\n''Columns in y: ',len(X.columns))


# # Splitting of training data and test datasets

# In[40]:


# sequencing of variable definition is important else there will be issue while fitting the model.
# try defining the training variables first and then the validation variables, you will find the error while fitting
# refer to the train_test_split documentation in scikit learn 

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)


# In[41]:


print(len(train_X),len(train_y),len(val_X),len(val_y))


# In[42]:


train_y.head()


# In[43]:


val_y.head()


# # Model definition

# In[44]:


iowa_model = DecisionTreeRegressor(random_state=1)


# # Fitting the model

# In[45]:


iowa_model.fit(train_X, train_y)


# # Making predictions on the validation dataset

# In[79]:


val_prediction = iowa_model.predict(val_X)


# # Evaluating the model performance by using the MAE quality metric

# In[58]:


val_mae = mean_absolute_error(val_prediction,val_y)
print("Validation MAE when not specifying max_leaf_nodes: {:,.0F}".format(val_mae))


# # The 'max_leaf_nodes' option in the DecisionTreeRegressor plays an impt
# # role in order to evaluate the model performance.
# > #### DecisionTreeRegressor suffers from overfitting and underfitting. The model performance can be controlled by observing 
# > #### the MAE for different set of 'max_leaf_nodes' and choosing the one which shows the minimum MAE

# In[76]:


# storing the leaf nodes in a list and defining a function which uses a for loop to find the MAE for different leafnodes

leaf_nodes = [5,50,100,200,400,500,700,1000]

# defining a function to obtain the MAE for different set of leaf nodes

def get_leaf_nodes(node,train_X,val_X,train_y,val_y):
    iowa_model = DecisionTreeRegressor(max_leaf_nodes = node, random_state=1)
    iowa_model.fit(train_X,train_y)
    va_pre = iowa_model.predict(val_X)
    va_mae = mean_absolute_error(va_pre,val_y)
    return(va_mae)

# using a dict comprehention to identify the MAE scores for different leaf nodes

scores = {nodes: get_leaf_nodes(nodes,train_X,val_X,train_y,val_y) for nodes in leaf_nodes}
print(scores)


# In[77]:


# using the minimum function to get the least value in the dictionary

best_score = min(scores, key=scores.get)
print(best_score)


# # Comparison of DecisionTreeRegressor models using 
#    >### (i) the default value in 'max_leaf_nodes'
#    >### (ii)the best vale in 'max_leaf_nodes' i.e. 100

# In[84]:


# model definition
iowa_model_def = DecisionTreeRegressor(random_state=1)
# model fitting (done with the feature training data and target training data)
iowa_model_def.fit(train_X,train_y)
# model prediction (done with the feature validation data)
val_pre_def = iowa_model_def.predict(val_X)
# model evaluation (done with the predicted data on feature validation dataset and the target validation data)
val_mae_def = mean_absolute_error(val_pre_def,val_y)
print('Validation MAE when not specifying the max_leaf_nodes: {:,.0F}'.format(val_mae_def))


# In[86]:


# model definition
iowa_model_best = DecisionTreeRegressor(max_leaf_nodes=100,random_state =1)
# model fitting with training (feature) data and training (target) data
iowa_model_best.fit(train_X,train_y)
# model prediction with validation (feature) data
val_pre_best = iowa_model_best.predict(val_X)
# evaluation of the model by comparing the predicted values and target validation data
val_mae_best = mean_absolute_error(val_pre_best,val_y)
print("Validation MAE after specifying the best 'max_leaf_node of 100': {:,.0F}".format(val_mae_best))


# In[ ]:




