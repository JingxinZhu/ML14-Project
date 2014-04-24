'''
This code is a part of the final project for course Machine Learning 
and Computational Statistics at NYU for Fall 2014.

Author: Bowei Zhang and Jingxin Zhu
Date created: 23rd, Apr
'''

import sys
import tweepy

class Crawler_Celebrity_Tweets:
    def crawl(self, n = 10, id_list = []):
        if len(id_list) == 0:
            print 'Please enter the list of IDs.'
        else:
            consumer_key = ''
            consumer_secret = ''
            access_token = ''
            access_token_secret = ''
            
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth)
            print api.user_timeline(id_list[0])

c = Crawler_Celebrity_Tweets()
c.crawl(id_list = ['psyclaudeZ'])
