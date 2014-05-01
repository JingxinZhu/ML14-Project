'''
File:

This file demos how to normalize featuer vectors.

'''

import sys
import feature_normalizer as fn

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


if __name__ == '__main__':
	main(sys.argv)
