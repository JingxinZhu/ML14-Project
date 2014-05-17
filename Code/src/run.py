'''
Update history:
    05/14: 
--------------------------------------------------------------------
This code is a part of the final project for course Machine Learning
and Computational Statistics at NYU for Fall 2014.

Author: Bowei Zhang and Jingxin Zhu
Date created: 30th, Apr
--------------------------------------------------------------------
'''
import sys

#import pydot
import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm
from sklearn import tree
from sklearn import ensemble
from sklearn import cross_validation

#import feature_normalizer as fn
import feature_normalizer_new as fn

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        print 'Usage: python main.py [# of celebrities] [# of tweets per ID]'\
                ' [output path]'

    n_ids = int(args[1])
    n_tweets_per_id = int(args[2])

    norm = fn.Feature_Normalizer()

    print 'Normalizing'
    #[labels, X] = norm.normalize(n_ids, n_tweets_per_id)
    [labels, X] = norm.normalize_with_topic(n_ids, n_tweets_per_id)

    # split test and training set
    print 'Spliting test and training set'
    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X,\
            labels, test_size = 0.3)

    # put aside test set for testing
    np.save('../data/X_test', X_test)
    np.save('../data/Y_test', Y_test)

    # Linear SVM
    print 'Linear SVM:'
    #cc = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    cc = [1.0]
    best = 0.0
    bestC = -1
    for c in cc:
        print 'c =', c
        svm_linear = svm.SVC(kernel = 'linear', C = c)
        svm_linear.fit(X_train, Y_train)
        scores = cross_validation.cross_val_score(svm_linear, X_train, Y_train)
        # validation scores
        print 'CV =', sum(scores) / 3
        if sum(scores) / 3 > best:
            best = sum(scores) / 3
            bestC = c
    svm_linear = svm.SVC(kernel = 'linear', C = bestC)
    svm_linear.fit(X_train, Y_train)
    print 'Test score:', svm_linear.score(X_test, Y_test)


    # Kernel SVM
    print 'Kernel SVM:'
    best = 0.0
    bestC = -1
    for c in cc:
        print 'c =', c
        svm_rbf = svm.SVC(kernel = 'rbf', C = 1)
        svm_rbf.fit(X_train, Y_train)
        print svm_rbf.score(X_train, Y_train)
        scores = cross_validation.cross_val_score(svm_rbf, X_train, Y_train)
        # validation
        print 'CV =', sum(scores) / 3
        if sum(scores) / 3 > best:
            best = sum(scores) / 3
            bestC = c
    svm_rbf = svm.SVC(kernel = 'rbf', C = bestC)
    svm_rbf.fit(X_train, Y_train)
    print 'Test score:', svm_rbf.score(X_test, Y_test)


    # Decision tree
    print 'Decision tree'
    tree_model = tree.DecisionTreeClassifier('entropy')
    s = []
    v = []
    best = 0.0
    bestD = -1
    for i in range(1, 10):
        print 'Depth =', i
        tree_model.set_params(max_depth = i)
        tree_model.fit(X_train, Y_train)
        ss = tree_model.score(X_train, Y_train)
        s.append(ss)
        scores = cross_validation.cross_val_score(tree_model, X_train, Y_train)
        # validation scores
        print 'CV =', sum(scores) / 3
        v.append(sum(scores) / 3)
        # validation
        if sum(scores) / 3 > best:
            best = sum(scores) / 3
            bestD = i
    tree_model = tree.DecisionTreeClassifier('entropy')
    tree_model.set_params(max_depth = bestD)
    tree_model.fit(X_train, Y_train)
    print 'Test score:', tree_model.score(X_test, Y_test)

    #p1, = plt.plot(range(1, 32), s, '-bs')
    #p2, = plt.plot(range(1, 32), v, '-r^')
    #plt.legend([p1, p2], ['Training Score', 'Validation Score'], loc = 3)
    #plt.title('Training and validation scores for different depths')
    #plt.show()

    #tree.set_params(max_depth = 5)
    #tree.fit(X_train, Y_train)
    #print tree.score(X_test, Y_test)
