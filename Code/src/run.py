#This code is a part of the final project for course Machine Learning
#and Computational Statistics at NYU for Fall 2014.

#Author: Bowei Zhang and Jingxin Zhu
#Date created: 30th, Apr

import sys

#import pydot
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

    print 'Normaling'
    [labels, X] = norm.normalize(n_ids, n_tweets_per_id)

    # split test and training set
    print 'Cross validating'
    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X,\
            labels, test_size = 0.3)

    # put aside test set for testing
    np.save('../data/X_test', X_test)
    np.save('../data/Y_test', Y_test)

    # Linear SVM
    print 'Linear SVM:'
    svm_linear = svm.SVC(kernel = 'linear', C = 1)
    svm_linear.fit(X_train, Y_train)
    print svm_linear.score(X_train, Y_train)
    scores = cross_validation.cross_val_score(svm_linear, X_train, Y_train)
    # validation scores
    print 'CV scores:', scores

    # Kernel SVM
    print 'Kernel SVM:'
    svm_rbf = svm.SVC(kernel = 'rbf', C = 1)
    svm_rbf.fit(X_train, Y_train)
    print svm_rbf.score(X_train, Y_train)
    scores = cross_validation.cross_val_score(svm_rbf, X_train, Y_train)
    # validation scores
    print 'CV scores:', scores

    # Decision tree
    print 'Decision Tree:'
    tree = tree.DecisionTreeClassifier('entropy')

    for i in range(1, 32):
        print '--Working on depth', i
        tree.set_params(max_depth = i)
        tree.fit(X_train, Y_train)
        print tree.score(X_train, Y_train)
        scores = cross_validation.cross_val_score(tree, X_train, Y_train)
        # validation scores
        print 'CV scores:', scores 
