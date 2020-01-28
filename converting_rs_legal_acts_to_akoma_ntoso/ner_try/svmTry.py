import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
# Read dataset to pandas dataframe

colnames = ["Sequence","Word","Lemma", "tag"]

dataset = pd.read_csv('datasetReldiS.csv', delimiter="\t", encoding="utf-8", names= colnames, skiprows= [0]) # ako ima imena kolona bez names=colnames



X = dataset.drop('tag', axis=1)
y = dataset['Word']

v = DictVectorizer(sparse=False)
X = v.fit_transform(X.to_dict('records'))
y = dataset.tag.values

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