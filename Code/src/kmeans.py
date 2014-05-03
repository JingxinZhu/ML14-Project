'''
File: 
'''

# Part I: initialization
import feature_normalizer_new as fn

n_ids = 4
n_tweets_per_id = 50
norm = fn.Feature_Normalizer()
#[labels, X] = norm.normalize(n_ids, n_tweets_per_id)
[labels, X] = norm.multiclass_normalize(n_tweets_per_id, 4)

# Part II: PCA analysis
m = len(X)
print m

