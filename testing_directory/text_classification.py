import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.preprocessing import LabelEncoder

our_data = pd.read_csv("F:/Data Science Books/More Books/Machine and Deep Learning/NLP/Full-Economic-News-DFE-839861.csv", encoding='latin-1')

# Step 1: train-test split
X = our_data.text
# the column text contains textual data to extract features from.
y = our_data.relevance
# this is the column we are learning to predict.
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

# ohe encoding in labels
### Preprocess Text
#Step 2-3: Pre-process and Vectorize train and test data
vect = CountVectorizer( max_features=5000) #Step-1
X_train_dtm = vect.fit_transform(X_train)#combined step 2 and 3
X_test_dtm = vect.transform(X_test)
print(X_train_dtm.shape, X_test_dtm.shape)

# # Naive Bayes Classifier
# nb = MultinomialNB() #instantiate a Multinomial Naive Bayes classifier
# nb.fit(X_train_dtm, y_train)#train the mode
# y_pred_class = nb.predict(X_test_dtm)#make class predictions for test data
#
# # LogReg Classifier
# logreg = LogisticRegression(class_weight="balanced", solver='liblinear')
# logreg.fit(X_train_dtm, y_train)
# y_pred_class = logreg.predict(X_test_dtm)
# print("Accuracy: ", accuracy_score(y_test, y_pred_class))

# svm classifier
classifier = LinearSVC(class_weight='balanced') #notice the “balanced” option
classifier.fit(X_train_dtm, y_train) #fit the model with training data
y_pred_class = classifier.predict(X_test_dtm)
print("Accuracy: ", accuracy_score(y_test, y_pred_class))