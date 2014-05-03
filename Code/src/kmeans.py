'''
File: 
'''

# Part I: initialization
import feature_normalizer_new as fn

n_ids = 10
n_tweets_per_id = 50
norm = fn.Feature_Normalizer()
[labels, X] = norm.normalize(n_ids, n_tweets_per_id)



# Part II: PCA analysis

