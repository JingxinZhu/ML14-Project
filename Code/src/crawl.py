'''
This code is a part of the final project for course Machine Learning 
and Computational Statistics at NYU for Fall 2014.

Author: Bowei Zhang and Jingxin Zhu
Date created: 24th, Apr
'''
#dsfdasdfa
import sys
import csv

import crawler_celebrity_accounts as cc
import crawler_celebrity_tweets as ct
import tweet_cleaner as tc

def main(args):
    if len(args) < 3:
        print 'Usage: python main.py [# of celebrities] [# of tweets per ID]'\
                ' [starting from ID]'

    # number of celebrities
    n_ids = 0
    start_id = 1
    # number of tweets per celebrity
    n_tweets_per_id = 0
    # folder to put the crawled data
    out_path = '../data'

    # parse the input
    try:
        n_ids = int(args[1])
        n_tweets_per_id = int(args[2])
        if len(args) > 3:
            start_id = int(args[3])
    except:
        print 'Error on the input parameters.'
        return 

    # initialize account crawler
    crawler_id = cc.Crawler_Celebrity_Accounts()
    id_list = crawler_id.crawl(n_ids, start_id)

    # initialize tweets crawler
    crawler_tweets = ct.Crawler_Celebrity_Tweets()
    tweets = crawler_tweets.crawl(n_tweets_per_id, id_list)

    # clean the raw data (but still need processing in later stage)
    cleaner = tc.Tweet_Cleaner()
    # use vec to store the results
    vec = []
    for i, t in enumerate(tweets):
        vec.append(cleaner.clean(t))

    # write to the disk
    with open(out_path + '/tweets', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(vec)

if __name__ == '__main__':
    main(sys.argv)
