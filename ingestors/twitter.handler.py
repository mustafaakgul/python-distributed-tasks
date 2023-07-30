# chcp 65001
# set PYTHONIOENCODING=utf-8


import twitter
import csv
import re
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CONSUMER_KEY = 'KsO0tcFDOyTikrnyDQyUulCUd'
CONSUMER_SECRET = 'agb9zIT6V4KgQoZV1yZb0EskwLfR6q84YJzJVjDPv7LQPtqNqT'
ACCESS_TOKEN = '723154990894735360-58WDj6K7jxqEa1O7Ckd9NN39LOvnWuT'
ACCESS_TOKEN_SECRET = 'pzdTEVTSnJrxQ9YzFHT829GUVUJw7Po5VOy2SIEduzT0p'


# Create an Api instance.authorize twitter, initialize tweepy
api = twitter.Api(
	consumer_key=CONSUMER_KEY,
	consumer_secret=CONSUMER_SECRET,
	access_token_key=ACCESS_TOKEN,
	access_token_secret=ACCESS_TOKEN_SECRET)


def get_all_tweets(screen_name):
	# initialize a list to add all the tweepy Tweets
	allTweets = []

	# make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.GetUserTimeline(screen_name=screen_name, count=200)

	# save most recent tweets
	allTweets.extend(new_tweets)

	# save the id of the oldest tweet less one
	oldest = allTweets[-1].id - 1

	# keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before {}".format(oldest))

		# all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.GetUserTimeline(screen_name=screen_name, count=200, max_id=oldest)

		# save most recent tweets
		allTweets.extend(new_tweets)

		# update the id of the oldest tweet less one
		oldest = allTweets[-1].id - 1

		print("...{} tweets downloaded so far".format(len(allTweets)))

		# delete the retweets
		cleaned_text = [re.sub(r'RT.*', '', i.text, flags=re.MULTILINE) for i in allTweets]

		# remove the @twitter mentions
		cleaned_text = [re.sub(r'@[\w]*', '', i, flags=re.MULTILINE) for i in cleaned_text]

		# transform the tweets into a 2D array that will populate the csv
		outtweets = [[tweet.id_str, tweet.created_at, cleaned_text[idx].encode('utf-8').decode('utf-8')] for idx, tweet in enumerate(allTweets)]

		# write the csv
		with open(os.path.join(BASE_DIR, 'djangoscrapy', 'data', 'raw', '{}_tweets.csv'.format(screen_name)), 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerow(["id", "created_at", "text"])
			writer.writerows(outtweets)


if __name__ == '__main__':
	# pass in the username of the account you want to download
	print(api.VerifyCredentials())
	users = api.GetFriends()
	get_all_tweets("mugayitimothy")
