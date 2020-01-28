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

df = pd.read_csv('datasetReldiS.csv', encoding="utf-8", sep="\t")

print(df.head())
print(df.isnull().sum())
df = df.fillna(method='ffill')  # fills the NaN's
df['Sentence #'].nunique(), df.Word.nunique(), df.Tag.nunique()

print(df.groupby('Tag').size().reset_index(name='counts'))  # distribution of tags

# X = df.drop(['Tag'], axis=1)
# v = DictVectorizer(sparse=False)
# X = v.fit_transform(X.to_dict('records'))
y = df.Tag.values
classes = np.unique(y)
classes = classes.tolist()
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state=0)
#print(X_train.shape, y_train.shape)

# per = Perceptron(verbose=10, n_jobs=-1, max_iter=5)
# per.partial_fit(X_train, y_train, classes)
#
# new_classes = classes.copy()
# new_classes.pop()
# print(new_classes)
#
#
# print(classification_report(y_pred=per.predict(X_test), y_true=y_test, labels=new_classes))

# sgd = SGDClassifier() # nema dovoljno memorije
# sgd.partial_fit(X_train, y_train, classes)
#
# new_classes = classes.copy()
# new_classes.pop()
# print(new_classes)
#
# print(classification_report(y_pred=sgd.predict(X_test), y_true=y_test, labels=new_classes))


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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)


crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(X_train, y_train)

new_classes = classes.copy()
new_classes.pop()
print(new_classes)

y_pred = crf.predict(X_test)
print(metrics.flat_classification_report(y_test, y_pred, labels = new_classes))


# def print_transitions(trans_features):
#     for (label_from, label_to), weight in trans_features:
#         print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))
# print("Top likely transitions:")
# print_transitions(Counter(crf.transition_features_).most_common(20))
# print("\nTop unlikely transitions:")
# print_transitions(Counter(crf.transition_features_).most_common()[-20:])
#
# def print_state_features(state_features):
#     for (attr, label), weight in state_features:
#         print("%0.6f %-8s %s" % (weight, label, attr))
# print("Top positive:")
# print_state_features(Counter(crf.state_features_).most_common(30))
# print("\nTop negative:")
# print_state_features(Counter(crf.state_features_).most_common()[-30:])

filename = "modelQ.sav"
pickle.dump(crf, open(filename, 'wb'))