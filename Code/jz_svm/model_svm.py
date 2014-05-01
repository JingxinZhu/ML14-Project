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
    filter_size = 5
    #matrix = np.zeros(USER_SIZE * (TWEETS_PER_USER - 2 * filter_size), len(vec[0,:])
    vec_matirx = np.array(vec)

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
                labels.append(-1)

        if num == 0:
            matrix = user_tweets
        else:
            matrix = np.concatenate((matrix, user_tweets), axis =0)
        
        #matrix = np.concatenate((matrix, user_tweets), axis = 0)
    labels = np.array(labels)
    #print sum(l == 1 for l in labels)
    return labels, matrix

# 3. normalize column by column, [min, max] -> [0,1]
def normalize(matrix):
    X = np.zeros(matrix.shape)
    print max(matrix[:,0])
    norm_column(matrix[0,:])
    #for i in range(len(matrix[0,:])):
    #for i in range(1):
        #col = matrix[:,i]
        #X[:,i] = norm_column(col)
    return X
            #X.append(norm_column(vec_matirx[:,i]))

# [min, max] -> [0, 1]
def norm_column(col):
    col_max = max(col)
    print col_max
    col_min = min(col)
    print col_min
    dis = col_max - col_min
    for v in col:
        if (dis != 0):
            v = 2 * (v - col_min) / dis - 1
    return col

# ------------------- #
#    Main function    #
# ------------------- #
USER_SIZE       = 2
TWEETS_PER_USER = 200
vec = read_tweets()
[labels, matrix] = label_vector(vec, USER_SIZE, TWEETS_PER_USER)
X = normalize(matrix) 
#print X[:,0]

#clf = svm.SVC()
#clf.fit(vec_matirx, labels)


