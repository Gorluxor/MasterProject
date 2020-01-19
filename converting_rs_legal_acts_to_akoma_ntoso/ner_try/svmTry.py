import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from ner_proba.word2vecAndrija import trainWrod2vec

#url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

# Assign colum names to the dataset

colnames = []
for i in range(0,300):
    colnames.append('word'+str(i+1))
colnames.append('class')

#colnames = ['word1','word2','word3','word4','word5', 'class']

# Read dataset to pandas dataframe
dataset = pd.read_csv('fastnumdataset.csv', delimiter=";", encoding="utf-8", names = colnames) # ako ima imena kolona bez names=colnames

X = dataset.drop('class', axis=1)
y = dataset['class']

#Train split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)


from sklearn.svm import SVC
svclassifier = SVC(kernel='rbf', degree=8) # probati i kernel="sigmoid" / kernel = 'rbf'
svclassifier.fit(X_train, y_train)

#customNumbersClasificationTry = [[6.7, 3, 5.2, 2.3]]
#labelReturned = svclassifier.predict(customNumbersClasificationTry)

#customNumbersClasificationTry = [["Kosovo"]]
#labelReturned = svclassifier.predict(customNumbersClasificationTry)

y_pred = svclassifier.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))