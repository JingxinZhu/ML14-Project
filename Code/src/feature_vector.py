'''
File: feature_vector.py
update history:
	05/09(jz): change feature vector's dimension corresponding to 
				timestamp's dividing into 6 separate columns.
--------------------------------------------------------------------
This code is a part of the final project for course Machine Learning 
and Computational Statistics at NYU for Fall 2014.

This file parse each row from datafile into one feature vector.

Author: Bowei Zhang and Jingxin Zhu
Date created: 29th, Apr
--------------------------------------------------------------------
'''

class Feature_Vector:
# omit 1,6,18 column, set value = 0 for these 3 columns
    def process(self, row = None):
    	try:
            dim = 27
            vec = [0] * dim
                
            # 0 - retweet count
            vec[0] = int(row[0])

            # 1. name of user
            #vec[1] = row[1]

            # 2 - account year
            vec[2] = int(row[2])
            # 3 - background picture enabled?
            vec[3] = self.label(row[3])
            # 4 - number of lists the user is in
            vec[4] = int(row[4])
            # 5 - number of followers the user has 
            vec[5] = int(row[5])

            # 6 - the language s/he is using
            #vec[6] = row[6]

            # 7 - geographical displayed?
            vec[7] = self.label(row[7])
            # 8 - verified?
            vec[8] = self.label(row[8])
            # 9 - number of tweets
            vec[9] = int(row[9])
            # 10 - number of followers
            vec[10] = int(row[10])

            # 11 - 17 - day it is tweeted
			# 18 - 23 - time period it is tweeted
            vec[11] = self.label(row[11])
            for i in range(11,24):
				vec[i] = self.label(row[i])

            # 19 - number of url includede in the tweet
            vec[24] = int(row[24])
            # 20 - number of hashtags used in the tweet
            vec[25] = int(row[25])
            # 21 - number of other users mentioned
            vec[26] = int(row[26])
            return vec
        except:
            print 'Unexpected format of input file'
            return []
    
    # set flat = 1 if true; -1 otherwise
    def label(self, flag):
        if (flag == 'True'):
            return 1
        else:
            return -1
