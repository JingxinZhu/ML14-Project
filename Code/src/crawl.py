'''
This code is a part of the final project for course Machine Learning 
and Computational Statistics at NYU for Fall 2014.

Author: Bowei Zhang and Jingxin Zhu
Date created: 24th, Apr
'''

import sys
import crawler_celebrity_accounts as cc
import crawler_celebrity_tweets as ct

def main(args):
    if len(args) < 3:
        print 'Usage: python main.py [# of celebrities] [# of tweets per ID]'\
                ' [output path]'

    # number of celebrities
    n_ids = 0
    # number of tweets per celebrity
    n_tweets_per_id = 0
    # folder to put the crawled data
    out_path = '../data'

    # parse the input
    try:
        n_ids = int(args[1])
        n_tweets_per_id = int(args[2])
        if len(args) > 3:
            out_path = args[3] 
            if out_path[-1] != '/':
                out_path += '/'
    except:
        print 'Error on the input parameters.'
        return 

    # initialize account crawler
    crawler_id = cc.Crawler_Celebrity_Accounts()
    id_list = crawler_id.crawl(n_ids)

    # initialize tweets crawler
    crawler_tweets = ct.Crawler_Celebrity_Tweets()
    tweets = crawler_tweets.crawl(n_tweets_per_id, id_list)

    for t in tweets:
        print t.retweet_count, t.user.name

if __name__ == '__main__':
    main(sys.argv)