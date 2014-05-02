'''
File:

This file demos how to normalize featuer vectors.

'''

import sys
import feature_normalizer as fn

from sklearn.svm import SVC 

def main(args):
	
	if len(args) < 2:
	    print 'Usage: python main.py [# of users] [# of tweets for each user]'
	
	# parse input command
	try:
	    user_size = int(args[1])
	    tweets_per_user = int(args[2]) 
	except:	
	    print 'Error on the input parameter.'
	    return
	
	# initialize 
	norm = fn.Feature_Normalizer()
	
	# main function
	[labels,X] = norm.normalize(user_size, tweets_per_user)
        
        ## simple test
        #X = X[:, 2:]

        ## split test and training set
        #X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X,\
                #labels, test_size = 0.3)

        ## put aside test set for testing
        #np.save('../data/X_test', X_test)
        #np.save('../data/Y_test', Y_test)

        ## SVM
        #print 'SVM:'
        #clf = svm.SVC(kernel = 'linear', C = 1)
        #clf.fit(X_train, Y_train)
        #print clf.score(X_train, Y_train)
        #scores = cross_validation.cross_val_score(clf, X_train, Y_train)
        ## validation scores
        #print 'CV scores:', scores


if __name__ == '__main__':
	main(sys.argv)
