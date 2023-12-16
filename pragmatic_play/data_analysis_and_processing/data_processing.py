from pragmatic_play.lib.data_objects import TestingObject

mode = "test"
testing_obj = TestingObject(mode=mode)

train_data = testing_obj.read_dataframe_from_csv(csv_path_to_read="D:/Machine_Learning_Projects/titanic_survival_classification/train_test_data/train.csv")
test_data = testing_obj.read_dataframe_from_csv(csv_path_to_read="D:/Machine_Learning_Projects/titanic_survival_classification/train_test_data/test.csv")

# Print Info
print("Train data info: {}".format(train_data.info()))
print("Test_data info: {}".format(test_data.info()))

# feature engineering
train_data_median_age = train_data['Age'].median()

train_data['Age'].fillna(train_data_median_age, inplace=True)
test_data['Age'].fillna(train_data_median_age, inplace=True)

train_data_median_fare = train_data.Fare.median()
test_data['Fare'].fillna(train_data_median_fare, inplace=True)

train_data.dropna(axis=0, subset=['Embarked'], inplace=True)
test_data.dropna(axis=0, subset=['Embarked'], inplace=True)


# drop Cabin from train and test
train_data = train_data.drop('Cabin', axis=1)
test_data = test_data.drop('Cabin', axis=1)

# Save Results
testing_obj.write_dataframe_to_csv(dataset=train_data, dataset_name="train_data_processed")
testing_obj.write_dataframe_to_csv(dataset=test_data, dataset_name="test_data_processed")
# proceed with modeling

