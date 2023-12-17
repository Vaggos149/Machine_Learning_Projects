import tensorflow as tf
import keras
import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from sklearn.model_selection import cross_validate, cross_val_score, GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from pragmatic_play.lib.sources_sinks import IO
from pragmatic_play.lib.modeling import TitanicClassification

# settings
mode = "testing"

# data processed reading

io = IO(mode=mode)


# model_engine = TitanicClassification()

# input dataframes
train_path_to_read = io.main_sink + '/train_data_processed.csv'
test_path_to_read = io.main_sink + '/test_data_processed.csv'

train_data = io.read_dataframe_from_csv(csv_path_to_read=train_path_to_read)
test_data = io.read_dataframe_from_csv(csv_path_to_read=test_path_to_read)

y_train_data = train_data.Survived
x_train_data = train_data.drop(['Survived'], axis=1)


X_train, X_test, y_train, y_test = train_test_split(x_train_data, y_train_data, test_size=0.33, random_state=42)


param_grid = {'n_neighbors': np.arange(1,10)}
knn_temp = KNeighborsClassifier()

