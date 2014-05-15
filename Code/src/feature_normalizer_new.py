'''
File: feature_normalizer_new.py
update history:
    05/09(jz): change function 'normalize' and 'multiclass_normalize' 
                by return X[:,2:]
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

    ## main function for two classes ##
    def normalize(self, user_size, tweets_num):
        t = 0 # flag indicating this is not dealing with topics
        [user_size,vec] = self.read_tweets(tweets_num)
        [labels, matrix] = self.label_vector(vec, user_size, tweets_num, t)
        # since max and min are deleted, we need to -10
        X = np.array(self.normalize_matrix(matrix, user_size, tweets_num - 10)) 
        return labels, X[:,2:]

    def normalize_with_topic(self, user_size, tweets_num):
        t = 1  # flag indicating dealing with topics
        [user_size,vec] = self.read_tweets(tweets_num)
        [labels, matrix, rowToDelete] = self.label_vector(vec, user_size, tweets_num, t)
        topic = np.load('../tmp/topic_matrix.npy')
        t = np.delete(topic, rowToDelete, axis = 0) 
        norm_X = np.array(self.normalize_matrix(matrix, user_size, tweets_num - 10)) 
        X = np.append(norm_X[:,2:], t, axis = 1) 
        return labels, X

    ## main function for multiple classes ##
    def multiclass_normalize(self, tweets_num, n_class):
        [user_size, vec] = self.read_tweets(tweets_num)
        [labels, matrix] = self.label_matrix(user_size, vec, tweets_num, n_class)
        X = np.array(self.normalize_matrix(matrix, user_size, tweets_num - 10))
        return labels, X[:,2:]

    # labels_matrix:
    # Output : labels, can be 1 to n_class, class 1 indicates most popular tweets, 
    #          class n_class implies least popular tweets. 
    def label_matrix(self, n_id, vec, n_tweets_per_id, n_class):
        labels = []
        filter_size = 5
        vec_matirx = np.array(vec)
        
        # create coefficients for different classes 
        factors = []
        for i in range(1, n_class):
            factor = (n_class - i) / float(n_class)
            factors.append(factor)
        
        # For each Twitter user, delete 5 tweets which have 5 highest retweets number
        # and delete 5 tweets which have 5 lowest retweets number.
        for num in range(n_id):
            # select tweets belonging to each user
            user_tweets = vec_matirx[n_tweets_per_id* num : n_tweets_per_id* (num + 1),:]
            col_retweet = user_tweets[:,0]

            # find 5 highest and 5 lowest retweets.
            max_5 = np.argsort(col_retweet)[-filter_size:]
            min_5 = np.argsort(col_retweet)[:filter_size]

            user_tweets = np.delete(user_tweets,[max_5,min_5],0)
            col_retweet = user_tweets[:,0]
            
            # create indicators to label feature vectors
            indicators = []
            for factor in factors:
                indicators.append( factor * (col_retweet.max()- col_retweet.min()) +\
                        col_retweet.min() )

            # label each feature vector
            for v in user_tweets:
                i = 0
                flag = 0
                while i < n_class-1:
                    if v[0] > indicators[i]:
                        flag = 1
                        labels.append(i+1)
                        break
                    i += 1
                if (flag == 0):
                    labels.append(n_class)

            #print indicators
            #print [v[0] for v in user_tweets]
            #print 'labels: ', labels

            # print ratio of each class
            #print '1st: %.4f ' % (float(sum(l==1 for l in labels)) / len(labels))
            #print '2st: %.4f ' % (float(sum(l==2 for l in labels)) / len(labels))
            #print '3st: %.4f ' % (float(sum(l==3 for l in labels)) / len(labels))
            #print '4st: %.4f ' % (float(sum(l==4 for l in labels)) / len(labels))

            # create new matrix
            if num == 0:
                matrix = user_tweets
            else:
                matrix = np.concatenate((matrix, user_tweets), axis =0)
        labels = np.array(labels)
        #return labels, matrix

    # 1. read in tweets from one user, process each tweet into a feature vector
    def read_tweets(self, t):
        # initialize raw data
        feature = fv.Feature_Vector()
        # use vec to store the results
        # data source
        #datafile = '../data/tweets'
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
        #print row_ct
        user_scale = row_ct / t
        return user_scale, vec

    # 2. label each feature vector after deleting the five hightest and five
    #    lowest retweets, 
    #    use 70% of highest number of retweets as indicator, 
    #    label a feature vecotor as 1 if vector's number of retweets is more than 70%
    #    label it as 0 otherwise.
    def label_vector(self, vec, user_size, tweets_num, t):

        labels = []
        filter_size = 5
        vec_matirx = np.array(vec)
        rowToDelete = []

        for num in range(user_size):
            # select tweets for each user
            user_tweets = vec_matirx[tweets_num * num : tweets_num * (num + 1),:]
            col_retweet = user_tweets[:,0]

            # find 5 highest and 5 lowest retweets.
            max_5 = np.argsort(col_retweet)[-filter_size:]
            min_5 = np.argsort(col_retweet)[:filter_size]
            
            if (t == 1):
                #a = np.append(max_5,min_5) 
                rowToDelete.append(max_5 + tweets_num * num)
                rowToDelete.append(min_5 + tweets_num * num)

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
        rowToDelete = np.asarray(rowToDelete).reshape(-1)
        #return labels, matrix
        if (t == 0):
            return labels, matrix
        else:
            return labels,matrix,rowToDelete

    # 3. normalize column by column, [min, max] -> [0,1]
    def normalize_matrix(self, matrix, user_size, tweets_number ):
        X = np.zeros(matrix.shape)
        # 3.1 for the 1st column, namely, retweets, normalize this column by user
        
        #print matrix.shape
        for num in range(user_size):
            col = matrix[tweets_number*num:tweets_number*(num+1),0] 
            #print 'col -', len(col), col
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

