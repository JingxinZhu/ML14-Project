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

import sys
import csv
import numpy as np
from sklearn import svm

import feature_vector as fv

# initialize raw data
feature = fv.Feature_Vector()
# use vec to store the results
vec = []
# data source
datafile = '../data/tweets'

# 1. read in tweets from one user, process each tweet into a feature vector
with open(datafile, 'rb') as f:
    reader = csv.reader(f, delimiter = ',')
    try:
        for row in reader:
            vec.append(feature.process(row))
    except csv.Error as e:
            sys.exit('file %s, line %d: %s',  (filename, reader.line_num, e))

# 2. label each feature vector:
#    use 70% of highest number of retweets as indicator, 
#    label a feature vecotor as 1 if vector's number of retweets is more than 70%
#    label it as 0 otherwise.

