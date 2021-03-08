from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time
from termcolor import colored
import datetime
import os
import tweepy
import sys
import json

class Tweeter:
    def __init__(self, STRINGVARS):
        API_KEY = STRINGVARS['API_KEY']
        API_SECRET = STRINGVARS['API_SECRET']
        ACCESS_TOKEN = STRINGVARS['ACCESS_TOKEN']
        ACCESS_SECRET = STRINGVARS['ACCESS_SECRET']

        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        self.api = tweepy.API(auth)
        self.callsign = colored('[Tweeter]', 'cyan') + ': '

    def tweet(self, tweet):
        self.save(tweet)
        try:
            with open('temp.txt', 'r') as f:
                self.api.update_status(f.read())
            print(self.callsign + 'Tweeted: ' + tweet)

        except tweepy.TweepError as e:
            print(self.callsign + e)

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


class CVSBot:
    def __init__(self, STRINGVARS):
        self.callsign = colored('[CVSBot]', 'magenta') + ': '
        print(self.callsign + 'Initializing Bot')
        self.CVS_URL = STRINGVARS['CVS_URL']
        self.WAITINGROOM_URL = STRINGVARS['WAITINGROOM_URL']
        self.SCREENER_URL = STRINGVARS['SCREENER_URL']
        self.TWEET_LINK = STRINGVARS['TWEET_LINK']
        self.MASS_BUTTON_XPATH = STRINGVARS['MASS_BUTTON_XPATH']
        self.UPDATE_TS_XPATH = STRINGVARS['UPDATE_TS_XPATH']
        self.CITIES_XPATH = STRINGVARS['CITIES_XPATH']
        self.STATUSES_XPATH = STRINGVARS['STATUSES_XPATH']
        self.FEEDBACK_BUTTON_XPATH = ['FEEDBACK_BUTTON_XPATH']
        print(type(self.FEEDBACK_BUTTON_XPATH))
        self.callsign = colored('[CVSBot]', 'magenta') + ': '
        self.last_update = None
        self.old_data = None
        self.then = None
        self.old_waitingroom_status = None
        self.available_locations = []
        self.Tweeter = Tweeter(STRINGVARS)
        self.tweets = {}
        self.driver = webdriver.Chrome()
        self.driver.set_window_position(-2000, 0)
        print(self.callsign + 'Initialized')

    def update(self):
        self.driver.get(self.CVS_URL)
        self.now = datetime.datetime.now().strftime("%I:%M %p")
        if self.now != self.then:
            print(self.callsign + 'Updating (' + self.now + ')')
        self.then = self.now
        try:
            self.driver.find_element_by_xpath(self.MASS_BUTTON_XPATH).click()
        
        except ElementClickInterceptedException:  # Deal with feedback box
            self.driver.find_element_by_xpath(self.FEEDBACK_BUTTON_XPATH).click()
            self.driver.find_element_by_xpath(self.MASS_BUTTON_XPATH).click()
        time.sleep(1)

        # Check Timestamp of Last update
        self.new_update = self.driver.find_element_by_xpath(self.UPDATE_TS_XPATH).text.split('.')[0][13:]
        if self.new_update != self.last_update:  # Found update, Initial path
            self.last_update = self.new_update
            print(self.callsign + colored('Found New Update @' +self.last_update, 'yellow'))
            print(self.callsign + colored('Checking For Availability', 'yellow'))

            self.cities = list(map(lambda el: el.text, self.driver.find_elements_by_xpath(self.CITIES_XPATH)))
            self.statuses = list(map(lambda el: el.text, self.driver.find_elements_by_xpath(self.STATUSES_XPATH)))
            self.new_data = dict(zip(self.cities, self.statuses))
            self.check_availability()
            if self.new_data == self.old_data:  # No change in data
                print(self.callsign + colored('No Change In Availability', 'red'))

            if self.new_data != self.old_data and self.old_data != None:  # Change in data
                self.old_data = self.new_data
                if len(self.available_locations) == 0:
                    print(self.callsign + colored('No Availability', 'red'))
            if len(self.available_locations) > 0:
                self.tweet_available_locations()

        self.driver.get(self.WAITINGROOM_URL)
        self.waitingroom_status = self.driver.current_url != self.SCREENER_URL
        if self.waitingroom_status != self.old_waitingroom_status:
            self.tweet_waitingroom_status()
        self.old_waitingroom_status = self.waitingroom_status

    def tweet_waitingroom_status(self):
        if self.waitingroom_status:
            print('Waiting Room Is Now ENABLED: ' + self.WAITINGROOM_URL)
        else:
            print('Waiting Room Is Now DISABLED')

    def tweet_available_locations(self):
        if len(self.available_locations) == 1:
            message = 'Available Location: \n' + self.available_locations[0] + '\n(as of' + self.last_update + ')'
        else:
            msg_bodies = []
            msg_body = ''
            for i in range(len(self.available_locations)):
                next_line = '\n' + self.available_locations[i]
                if len(msg_body + next_line) < 230:
                    msg_body += next_line
                    continue
                else:
                    msg_bodies.append(msg_body)
                    msg_body = ''
    
            if len(msg_bodies) == 1:
                message = 'Available Locations: ' + msg_bodies[0] + '\n(as of' + self.last_update + ')'
            else:
                first_msg = 'Available Locations: ' + msg_bodies[0] + '\n(as of' + self.last_update + ')' + '\n(1/' + str(len(msg_bodies)) + ')'
                aux_bodies = msg_bodies[2:]
                self.Tweeter.tweet(first_msg)
                first_msg_id = self.Tweeter.last_tweet_id()
                for body in aux_bodies:
                    message = 'Available Locations: ' + body + '\n(as of' + self.last_update + ')' + '\n('+str(aux_bodies.index(body))+'/' + str(len(msg_bodies)) + ')'
                    self.Tweeter.reply(message, first_msg_id)

    def check_availability(self):
        self.old_available_locations = self.available_locations
        self.available_locations = []
        for i in self.new_data:
            if self.new_data[i] == 'Available':
                self.available_locations.append(i.split(',')[0])
                if i not in self.old_available_locations:
                    print(self.callsign + i + 'Is Now ' + colored('AVAILABLE','green') + ' as of ' + self.new_update)
        for i in self.old_available_locations:
            if i not in self.available_locations:
                print(self.callsign + i + 'Is Now ' + colored('UNAVAILABLE','green') + ' as of ' + self.new_update)

    def save(message):
        with open('temp.txt', 'w') as f:
            f.write(message)


def run(event=None, context=None):
    running = True
    with open('STRINGVARS.json') as f:
        STRINGVARS = json.load(f)
    print(STRINGVARS)
    bot = CVSBot(STRINGVARS)
    while running:
        bot.update()
        time.sleep(3)
run()
