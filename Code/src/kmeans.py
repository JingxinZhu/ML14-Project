'''
File: 
'''
import numpy as np
from sklearn.decomposition import PCA

import feature_normalizer_new as fn

# Part I: initialization

n_ids = 15
n_tweets_per_id = 150 
n_feature = 22
norm = fn.Feature_Normalizer()
#[labels, X] = norm.normalize(n_ids, n_tweets_per_id)
[labels, X] = norm.multiclass_normalize(n_tweets_per_id, 4)


# Part II: PCA analysis
def PCA_analysis(X):
	U,s,V = np.linalg.svd(X, full_matrices = True)
	S = np.zeros((len(X), n_feature))
	S[:n_feature, :n_feature] = np.diag(s)
