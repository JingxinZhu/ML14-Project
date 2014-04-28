'''
This code is a part of the final project for course Machine Learning 
and Computational Statistics at NYU for Fall 2014.

Author: Bowei Zhang and Jingxin Zhu
Date created: 23rd, Apr
'''

import tweepy

class Crawler_Celebrity_Tweets:
    # n_per_user denotes how many tweets to acquire for each user
    def crawl(self, n_per_user = 10, id_list = []):
        tweet_list = []
        if len(id_list) == 0:
            print 'Please enter the list of IDs.'
        else:
            api = tweepy.API()
            try:
                # necessary params to get access to Twitter API
                consumer_key = '3yvyOFJ1TYwiFtB2qTTpA'
                consumer_secret = 'OFiVTr0FVu5YcRQcNoKvWF26x04uBUkz8ZNoBX5Dr2s'
                access_token ='297845201-SrnlyPVGXEiDsdZ9sUBrNTQ0IMgqRFCJBecxWBdS' 
                access_token_secret = '3nKDHHluqmC4PYq56Q3szKYQA5LrOGD1AcFmm6Q'
                
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
            except:
                print 'Failed to get through authentication.'
                return tweet_list

            # initialize the API object using keys
            api = tweepy.API(auth)

            for user in id_list:
                try:
                    tweets = api.user_timeline(user, count = n_per_user)
                    tweet_list += tweets
                    #for t in tweets:
                    #    print t.retweet_count
                except:
                    print 'User', user, 'does not exist.'
            
        return tweet_list
