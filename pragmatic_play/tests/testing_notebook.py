import pandas as pd
import numpy as np
import nltk
import sklearn
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from pragmatic_play.data_objects import TestingObject

mode = "test"
testing_obj = TestingObject(mode=mode)

train_data = testing_obj.read_dataframe_from_csv(csv_path_to_read="D:/Machine_Learning_Projects/titanic_survival_classification/train_test_data/train.csv")
test_data = testing_obj.read_dataframe_from_csv(csv_path_to_read="D:/Machine_Learning_Projects/titanic_survival_classification/train_test_data/test.csv")

# A. DATA EXPLORATION

## Print Info
print("Train data info: {}".format(train_data.info()))
print("Test_data info: {}".format(test_data.info()))

## Visualize columns
sns.lmplot(x="Age", y="Fare", data=train_data)
sns.boxplot(data=train_data, x="Survived", y="Fare", hue="Pclass")
plt.show()

## Analyze data, write comments
# OK, clear advantage for the rich, seems like the probability of surviving is dependent on your class...
# women survive more
# do children? Probably yes --> Seems like it doesnt, needs further checking for statistical significance
### etc etc etc
# mpourou mpourou sthn plateia koumoundourou


## Replace null values
# Pame ena replace na teleiwnoume

# feature engineering
# median imputation for aGE IS FINE,
train_data_median_age = train_data['Age'].median()

train_data['Age'].fillna(train_data_median_age, inplace=True)
test_data['Age'].fillna(train_data_median_age, inplace=True)

train_data_median_fare = train_data.Fare.median()
test_data['Fare'].fillna(train_data_median_fare, inplace=True)
# most frequent for Embarked is fine, but since there are only two missing vlaues, we will simply drop the rows.
train_data.dropna(axis=0, subset=['Embarked'], inplace=True)
test_data.dropna(axis=0, subset=['Embarked'], inplace=True)
# drop Cabin from train and test
train_data = train_data.drop('Cabin', axis=1)
test_data = test_data.drop('Cabin', axis=1)

# repeat results for train and test set

## Save Results
testing_obj.write_dataframe_to_csv(dataset=train_data, dataset_name="train_data_processed")
testing_obj.write_dataframe_to_csv(dataset=test_data, dataset_name="test_data_processed")
# proceed with modeling
# Random Forest, Dense Network, xgb
