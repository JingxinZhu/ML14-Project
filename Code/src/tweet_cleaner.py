'''
File: tweet_cleaner.py
update history:
    05/09(jz): divide timestamp into 6 time zones(first is (7am,11am]), 
                thus enlarging feature dimensions from 22 to 27.  
--------------------------------------------------------------------
This code is a part of the final project for course Machine Learning 
and Computational Statistics at NYU for Fall 2014.

Author: Bowei Zhang and Jingxin Zhu
Date created: 28th, Apr
--------------------------------------------------------------------
'''
# please refer to the project notes for each feature in the vector
class Tweet_Cleaner:
    def clean(self, tw = None):
        try:
            # may be changed later, this INCLUDES the label as well as user name!
            dim = 27 
            vec = [False] * dim 
            
            # 0 - retweet count
            vec[0] = int(tw.retweet_count)
            # 1 - user name
            vec[1] = tw.user.name.encode('utf-8')
            # 2 - account year
            vec[2] = 2014 - tw.user.created_at.year 
            # 3 - background picture enabled?
            vec[3] = tw.user.profile_background_tile
            # 4 - number of lists the user is in
            vec[4] = tw.user.listed_count
            # 5 - number of followers the user has 
            vec[5] = tw.user.followers_count
            # 6 - the language s/he is using
            vec[6] = tw.user.lang
            # 7 - geographical displayed?
            vec[7] = tw.user.geo_enabled
            # 8 - verified?
            vec[8] = tw.user.verified
            # 9 - number of tweets
            vec[9] = tw.user.statuses_count
            # 10 - number of followers
            vec[10] = tw.user.friends_count
            # 11 - 17 - day it is tweeted
            vec[11 + tw.created_at.weekday()] = True
            # 18 - timestampe when it was tweeted, UTC +0000 
            timestamp = self.set_time(int(tw.created_at.hour)) 
            vec[timestamp] = True 
            #vec[18] = tw.created_at.hour * 3600 + tw.created_at.minute * 60 +\
            			#tw.created_at.second
            # 19 - number of url includede in the tweet
            vec[24] = len(tw.entities.get('urls'))
            # 20 - number of hashtags used in the tweet  
            vec[25] = len(tw.entities.get('hashtags'))
            # 21 - number of other users mentioned
            vec[26] = len(tw.entities.get('user_mentions'))
            
            with open('../data/corpus', 'a') as f:
                tokens = tw.text.encode('utf-8').splitlines()
                s = ''
                for t in tokens:
                    s += t + ' '
                f.write(s + '\n')
            return vec
        except:
            print 'Please input a tweet in correct format.'
            return []

    def set_time(self, hour):
        if hour >=1 and hour < 5:
            return 21
        if hour >=5 and hour < 9: 
            return 22
        if hour >=9 and hour < 13: 
            return 23
        if hour >=13 and hour < 17: 
            return 18 
        if hour >=17 and hour < 21: 
            return 19 
        if hour >=21 or hour==0: 
            return 20 

#c = Tweet_Cleaner()
#print c.clean()

