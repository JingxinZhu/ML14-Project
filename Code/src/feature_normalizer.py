'''
File: feature_normalizer.py
update history:
	05/09(jz): temporarily set datafile = '../data/tweets' for
				'../data/tweets_full' has not been updated since
				feature vector's dimension enlarged to 27.
	05/09(bw): change function 'normalize' by return X[:,2:]
--------------------------------------------------------------------
This code is a part of the final project for course Machine Learning 
and Computational Statistics at NYU for Fall 2014.

Goal  : This file normalize feature vectors to [-1, 1].
Input : user_size  -number of Twitter users chosen for models.   
        tweets_num -number of tweets selected from each Twitter user.
Output: labels     -array of labels for each feature vector, 
                    'popular' tweets is labeled as 1, 0 otherwise.
        X          -array of n-by-m, containing m normalized feature
                    vectors, each of which has n features.

Author: Bowei Zhang and Jingxin Zhu
Date created: 29th, Apr
--------------------------------------------------------------------
'''

import sys
import csv
import numpy as np

import feature_vector as fv

class Feature_Normalizer:

    ## main function ##
    def normalize(self, user_size, tweets_num):
        [user_size,vec] = self.read_tweets(tweets_num)
        [labels, matrix] = self.label_vector(vec, user_size, tweets_num)

        # since max and min are deleted, we need to -10
        X = np.array(self.normalize_matrix(matrix, user_size, tweets_num - 10)) 
        return labels, X[:, 2:]

    # 1. read in tweets from one user, process each tweet into a feature vector
    def read_tweets(self, t):
        # initialize raw data
        feature = fv.Feature_Vector()
        # use vec to store the results
        # data source
        datafile = '../data/tweets_full'
        vec = []
        row_ct = 0
        with open(datafile, 'rb') as f:
            reader = csv.reader(f, delimiter = ',')
            try:
                for row in reader:
                    vec.append(feature.process(row))
                    row_ct += 1
            except csv.Error as e:
                sys.exit('file %s, line %d: %s',  (filename, reader.line_num, e))
        user_scale = row_ct / t
        return user_scale, vec

    # 2. label each feature vector after deleting the five hightest and five
    #    lowest retweets, 
    #    use 70% of highest number of retweets as indicator, 
    #    label a feature vecotor as 1 if vector's number of retweets is more than 70%
    #    label it as 0 otherwise.
    def label_vector(self, vec, user_size, tweets_num):
        labels = []
        filter_size = 5
        vec_matirx = np.array(vec)

        for num in range(user_size):
            # select tweets for each user
            user_tweets = vec_matirx[tweets_num * num : tweets_num * (num + 1),:]
            col_retweet = user_tweets[:,0]

            # find 5 highest and 5 lowest retweets.
            max_5 = np.argsort(col_retweet)[-filter_size:]
            min_5 = np.argsort(col_retweet)[:filter_size]

            user_tweets = np.delete(user_tweets,[max_5,min_5],0)
            col_retweet = user_tweets[:,0]

            # 70% * (max_after_deleted_top_5 - min_after_deleted_down_5)
            indicator = 0.7 * (col_retweet.max()- col_retweet.min()) +\
                    col_retweet.min()

            # label each feature vector
            for v in user_tweets:
                if v[0] > indicator:
                    labels.append(1)
                else:
                    labels.append(-1)
            
            # create new matrix, which has deleted top 5 and low 5 retweets row. 
            if num == 0:
                matrix = user_tweets
            else:
                matrix = np.concatenate((matrix, user_tweets), axis =0)
            
            #print sum(l == 1 for l in labels)
        labels = np.array(labels)
        return labels, matrix

    # 3. normalize column by column, [min, max] -> [0,1]
    def normalize_matrix(self, matrix, user_size, tweets_number ):
        X = np.zeros(matrix.shape)
        # 3.1 for the 1st column, namely, retweets, normalize this column by user
        
        for num in range(user_size):
            col = matrix[tweets_number*num:tweets_number*(num+1),0] 
            X[tweets_number*num:tweets_number*(num+1) ,0] = self.norm_column(col)
            
        # 3.2 for the rest columns, normalize by column
        for i in range(1, len(X[0,:])):
            col = matrix[:,i]
            X[:,i] = self.norm_column(col)
        return X

    # 4.[min, max] -> [0, 1]
    def norm_column(self, col):
        col_return = []
        col_max = col.max()
        col_min = col.min()
        dis = col_max - col_min
        for v in col:
            if (dis != 0):
                v = 2 * (float(v - col_min)) / dis - 1
            else: 
                v = 0
            col_return.append(v)
        return col_return

