import pandas as pd
from feature_engine.imputation import MeanMedianImputer
train_dataset = pd.read_csv("titanic_survival_classification/train_test_data/train.csv")

train_dataset.info()

median_imputer = MeanMedianImputer(imputation_method='median', variables=['Age'])
results = median_imputer.fit(train_dataset).transform(train_dataset)
results.info()
