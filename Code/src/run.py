'''
This code is a part of the final project for course Machine Learning 
and Computational Statistics at NYU for Fall 2014.

Author: Bowei Zhang and Jingxin Zhu
Date created: 30th, Apr
'''

import sys

import pydot
import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm
from sklearn import tree
from sklearn import ensemble
from sklearn import cross_validation

import feature_normalizer as fn

def visualize_error(scores = [1.00, 0.57], labels = ['a', 'b']):
    fig = plt.figure()

    width = .5
    n = len(scores)
    ind = np.arange(n)
    plt.bar(ind, scores)

    x = range(n)
    plt.xticks(ind, labels)

    plt.show()

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        print 'Usage: python main.py [# of celebrities] [# of tweets per ID]'\
                ' [output path]'

    n_ids = int(args[1])
    n_tweets_per_id = int(args[2])

    norm = fn.Feature_Normalizer()

    [labels, X] = norm.normalize(n_ids, n_tweets_per_id)

    # split test and training set
    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X,\
            labels, test_size = 0.3)

    # put aside test set for testing
    np.save('../data/X_test', X_test)
    np.save('../data/Y_test', Y_test)

    # SVM
    clf = svm.SVC(kernel = 'linear', C = 1)
    clf.fit(X_train[:, 2:], Y_train)

    scores = cross_validation.cross_val_score(clf, X_train[:, 2:], Y_train)
    # validation scores
    print scores
