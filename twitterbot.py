import json
import tweepy
from termcolor import colored

class Tweeter:
    def __init__(self):
        with open("twitter_creds.json") as f:  
            twitter_creds = json.load(f)
        twitter_creds = dict(twitter_creds)
        API_KEY = twitter_creds['API_KEY']
        API_SECRET = twitter_creds['API_SECRET']
        ACCESS_TOKEN = twitter_creds['ACCESS_TOKEN']
        ACCESS_SECRET = twitter_creds['ACCESS_SECRET']

        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        self.api = tweepy.API(auth)
        self.callsign = colored('[Tweeter]', 'cyan') + ': '
    
    def save(self, message):
        with open('temp.txt', 'w') as f:
            f.write(message)
            
    def tweet(self, tweet):
        self.save(tweet)
        try:
            with open('temp.txt', 'r') as f:
                self.api.update_status(f.read())
            print(self.callsign + 'Tweeted: ' + tweet)

        except tweepy.TweepError as e:
            print(self.callsign + str(e))

    def reply(self, tweet, tweet_id):
        self.save(tweet)
        try:
            with open('temp.txt', 'r') as f:
                self.api.update_status(status=f.read(
                ), in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
                print(self.callsign + 'Tweeted: ' + tweet)
        except tweepy.TweepError as e:
            print(self.callsign + e)

    def last_tweet_id(self):
        return self.api.user_timeline()[0].id

    def last_tweet_text(self):
        return self.api.user_timeline()[0].text

