#
# import pandas as pd
# import numpy as np
# from sklearn.feature_extraction import DictVectorizer
# from sklearn.feature_extraction.text import HashingVectorizer
# from sklearn.linear_model import Perceptron
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import SGDClassifier
# from sklearn.linear_model import PassiveAggressiveClassifier
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.metrics import classification_report
# import pickle
#
#
# df = pd.read_csv('datasetReldiS.csv', encoding="utf-8", sep="\t")
# print(df.head())
# print(df.isnull().sum())
# df = df.fillna(method='ffill')  # fills the NaN's
# df['Sentence #'].nunique(), df.Word.nunique(), df.Tag.nunique()
#
# print(df.groupby('Tag').size().reset_index(name='counts'))  # distribution of tags
#
# X = df.drop(['Tag'], axis=1)
# v = DictVectorizer(sparse=False)
# X = v.fit_transform(X.to_dict('records'))
# y = df.Tag.values
# classes = np.unique(y)
# classes = classes.tolist()
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)
# print(X_train.shape, y_train.shape)


import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import pickle

df = pd.read_csv('datasetHr.csv', encoding="utf-8", sep="\t")

print(df.head())
print(df.isnull().sum())
df = df.fillna(method='ffill')  # fills the NaN's
df['Sentence #'].nunique(), df.Word.nunique(), df.Tag.nunique()

print(df.groupby('Tag').size().reset_index(name='counts'))  # distribution of tags

y = df.Tag.values
classes = np.unique(y)
classes = classes.tolist()


import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
from collections import Counter


class SentenceGetter(object):

    def __init__(self, data):
        self.n_sent = 1
        self.data = data
        self.empty = False
        agg_func = lambda s: [(w, p, t) for w, p, t in zip(s['Word'].values.tolist(),
                                                           s['Pos'].values.tolist(),
                                                           s['Tag'].values.tolist())]
        self.grouped = self.data.groupby('Sentence #').apply(agg_func)
        self.sentences = [s for s in self.grouped]

    def get_next(self):
        try:
            s = self.grouped['Sentence: {}'.format(self.n_sent)]
            self.n_sent += 1
            return s
        except:
            return None


getter = SentenceGetter(df)
sentences = getter.sentences


def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True
    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        postag1 = sent[i + 1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, postag, label in sent]


def sent2tokens(sent):
    return [token for token, postag, label in sent]


X = [sent2features(s) for s in sentences]
y = [sent2labels(s) for s in sentences]
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1, random_state=0)
X_test = X
y_test = y
filename = 'model.sav'
crf = loaded_model = pickle.load(open(filename, 'rb'))
y_pred = crf.predict(X_test)
new_classes = classes.copy()
new_classes.pop()
print(new_classes)

#y_pred = crf.predict(X_test)
#print(metrics.flat_classification_report(y_test, y_pred, labels = new_classes))

print(metrics.flat_classification_report(y_test, y_pred, labels=new_classes))

result = loaded_model.score(X_test, y_test)
print("Overall: ", str(result))
