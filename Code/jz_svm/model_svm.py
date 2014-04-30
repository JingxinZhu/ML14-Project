'''
File: model_svm.py
--------------------------------------------------------------------
This code is a part of the final project for course Machine Learning 
and Computational Statistics at NYU for Fall 2014.

This file implements SVM method.

Author: Bowei Zhang and Jingxin Zhu
Date created: 29th, Apr
--------------------------------------------------------------------
'''

# 1. do not use most recent five because they might be active

import sys
import csv
import numpy as np
from sklearn import svm

import feature_vector as fv


# 1. read in tweets from one user, process each tweet into a feature vector
def read_tweets():
    # initialize raw data
    feature = fv.Feature_Vector()
    # use vec to store the results
    # data source
    datafile = '../data/tweets'
    vec = []
    with open(datafile, 'rb') as f:
        reader = csv.reader(f, delimiter = ',')
        try:
            for row in reader:
                vec.append(feature.process(row))
        except csv.Error as e:
            sys.exit('file %s, line %d: %s',  (filename, reader.line_num, e))
    return vec

# 2. label each feature vector: after deleting the five hightest and five
#    lowest retweets, 
#    use 70% of highest number of retweets as indicator, 
#    label a feature vecotor as 1 if vector's number of retweets is more than 70%
#    label it as 0 otherwise.
def label_vector(vec, USER_SIZE, TWEETS_PER_USER):
    labels = []
    matrix = []
    vec_matirx = np.array(vec)
    filter_size = 5

    for num in range(USER_SIZE):
        # select tweets for each user
        user_tweets = vec_matirx[TWEETS_PER_USER*num : TWEETS_PER_USER+TWEETS_PER_USER*num,:]
        col_retweet = user_tweets[:,0]

        # find 5 highest and 5 lowest retweets.
        max_5 = np.argsort(col_retweet)[-filter_size:]
        min_5 = np.argsort(col_retweet)[:filter_size]

        user_tweets = np.delete(user_tweets,[max_5,min_5],0)
        col_retweet = user_tweets[:,0]

        # Option 1: 70% of max_after_deleted_top_5
        #indicator = 0.7 * max(col_retweet)
        # Option 2: 70% (max_after_deleted_top_5 - min_after_deleted_down_5)
        indicator = 0.7 * (max(col_retweet) - min(col_retweet))

        # label each feature vector
        for v in user_tweets:
            if v[0] > indicator:
                labels.append(1)
            else:
                labels.append(0)
        matrix.append(user_tweets)   
    labels = np.array(labels)
    #print sum(l == 1 for l in labels)
    print matrix
    return labels, matrix

# 3. normalize column by column
def normalize(vec_matirx):
    X = np.zeros(vec_matirx.shape)
    for i in range(len(vec_matirx)):
        col = vec_matirx[:,i]
        col_max = max(col)
        col_min = min(col)
        #if col_max * col_min == 0:
            #X.append(norm_column(vec_matirx[:,i]))


def norm_column(col):
    return  0

# ------------------- #
#    Main function    #
# ------------------- #
USER_SIZE       = 2
TWEETS_PER_USER = 200
vec = read_tweets()
[labels, vec_matirx] = label_vector(vec, USER_SIZE, TWEETS_PER_USER)
#X = normalize(vec_matirx) 

#clf = svm.SVC()
#clf.fit(vec_matirx, labels)


