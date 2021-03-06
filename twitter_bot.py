#!/usr/bin/python3.6
""" A Twitter bot that follows followers, retweets and replies based on certain keywords. 

Get your own API keys by signing up on http://developer.twitter.com.
"""
import tweepy
from time import sleep

class App:
    def __init__(self,
                 keywords = None,
                 CONSUMER_KEY = 'consumer_key',
                 CONSUMER_SECRET = 'consumer_secret',
                 ACCESS_KEY = 'access_key',
                 ACCESS_SECRET = 'access_secret'):

        self.CONSUMER_KEY = CONSUMER_KEY
        self.CONSUMER_SECRET = CONSUMER_SECRET
        self.ACCESS_KEY = ACCESS_KEY
        self.ACCESS_SECRET = ACCESS_SECRET
        self.keywords = keywords

        # Create an api object
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

        # Run main()
        self.main()


    def main(self):
        while True:
            APP_PAUSE_TIME = 5 * 60
            if self.keywords is not None:
                self.retweet_keyword(self.keywords)
            sleep(APP_PAUSE_TIME)


    def follow_followers(self):
        print('Looking for followers to follow.')
        for follower in tweepy.Cursor(self.api.followers).items():
            try:
                follower.follow()

            except tweepy.TweepError as e:
                print(e.reason)


    def retweet_keyword(self, keywords, num_tweets=10):
        print('\nLooking for tweets with matched keywords to RT.')
        for tweet in tweepy.Cursor(self.api.search, self.keywords).items(num_tweets):
            try:
                username = tweet.user.screen_name
                tweet.retweet()
                print('Retweeted tweet: ' + username)

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break


    def favorite_keyword(self, keywords, num_tweets=10):
        print('Looking for tweets with matched keywords to favorite.')
        for tweet in tweepy.Cursor(self.api.search, self.keywords).items(num_tweets):
            try:
                username = tweet.user.screen_name
                tweet.favorite()
                print('Favorite tweet: ' + username)

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break


    def reply_keyword(self, keywords, num_tweets=5, phrase=None):
        print('Looking for tweets with matched keywords to reply.')
        for tweet in tweepy.Cursor(self.api.search, self.keywords).items(num_tweets):
            try:
                tweetId = tweet.user.id
                username = tweet.user.screen_name
                self.api.update_status('@' + username + ' ' + phrase,
                                  in_reply_to_status_id = tweetId)
                print ('Replied to ' + username + ': ' + phrase)

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break


if __name__ == '__main__':
    app = App(keywords=('#DataScience OR #MachineLearning OR #NaturalLanguageProcessing OR #DeepLearning OR #NeuralNetwork OR #NeuralNetworks'))