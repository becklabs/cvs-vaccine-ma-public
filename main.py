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
import dill

class Tweeter:
    def __init__(self):
        API_KEY = 'API_KEY'
        API_SECRET = 'API_SECRET'
        ACCESS_TOKEN = 'ACCESS_TOKEN'
        ACCESS_SECRET = 'ACCESS_SECRET'

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

class SmallState:
    def __init__(self):
        pass
    
    def update(self, bot):
        self.last_update = bot.last_update
        self.old_data = bot.old_data
        self.then = bot.then
        self.available_locations = bot.available_locations
        self.old_waitingroom_status = bot.old_waitingroom_status
        with open('smallstate.pkl', 'wb') as dill_file:
            dill.dump(self, dill_file)
            
    def retrieve(self):
        try:
            with open('smallstate.pkl', 'rb') as dill_file:
                saved_state = dill.load(dill_file)
            self.last_update = saved_state.last_update
            self.old_data = saved_state.old_data
            self.then = saved_state.then
            self.available_locations = saved_state.available_locations
            self.old_waitingroom_status = saved_state.old_waitingroom_status
            return True
        except FileNotFoundError:
            return False
class CVSBot:
    def __init__(self):
        self.callsign = colored('[CVSBot]', 'magenta') + ': '
        print(self.callsign + 'Initializing Bot')
        self.CVS_URL = 'https://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-link2-coronavirus-vaccine#'
        self.TWEET_LINK = 'https://www.cvs.com/vaccine/intake/store/cvd-schedule.html?icid=coronavirus-lp-vaccine-sd-statetool'
        self.WAITINGROOM_URL = 'https://cvs.com/vaccine/intake/store/cvd-schedule.html?icid=coronavirus-lp-vaccine-sd-statetool'
        self.SCREENER_URL = 'https://www.cvs.com/vaccine/intake/store/covid-screener/covid-qns'
        self.MASS_BUTTON_XPATH = '//*[@id="empty-0d710bd9ab"]/content/div/div/div/div[3]/div/div/div[2]/div/div[5]/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div/div/div/div[2]/ul/li[2]'
        self.UPDATE_TS_XPATH = '//*[@id="vaccineinfo-MA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[5]/div'
        self.CITIES_XPATH = '//*[@id="vaccineinfo-MA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table/tbody/tr/td[1]'
        self.STATUSES_XPATH = '//*[@id="vaccineinfo-MA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table/tbody/tr/td[2]'
        self.FEEDBACK_BUTTON_XPATH = '//*[@id="acsMainInvite"]/div/a[1]'
        self.callsign = colored('[CVSBot]', 'magenta') + ': '
        self.small = SmallState()
        print(self.callsign + 'Searching For Saved State')
        saved_state = self.small.retrieve()
        if saved_state:
            print(self.callsign + 'Found Saved State, Loading')
            self.last_update = self.small.last_update
            self.old_data = self.small.old_data
            self.then = self.small.then
            self.available_locations = self.small.available_locations
            self.old_waitingroom_status = self.small.old_waitingroom_status
        else:
            print(self.callsign + 'Failed To Find Saved State')
            self.last_update = None
            self.old_data = None
            self.then = None
            self.available_locations = []
            self.old_waitingroom_status = None
            
        self.Tweeter = Tweeter()
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
            if self.new_data == self.old_data and self.old_data != None:  # No change in data
                print(self.callsign + colored('No Change In Availability', 'red'))

            if self.new_data != self.old_data:  # Change in data
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
        self.small.update(self)
    def tweet_waitingroom_status(self):
        if self.waitingroom_status:
            print(self.callsign + colored('Waiting Room Is Now ACTIVE', 'green')+'(as of '+self.last_update+')')
            message = 'Waiting Room Is Now ACTIVE'+'\n(as of '+self.last_update+')'
            self.Tweeter.tweet(message)
        else:
            print(self.callsign + colored('Waiting Room Is Now DISABLEED', 'red'))
            message = 'Waiting Room Is Now DISABLED'+' (as of '+self.last_update+') '+self.WAITINGROOM_URL
            self.Tweeter.tweet(message)

    def tweet_available_locations(self):
        if len(self.available_locations) == 1:
            message = 'Available Location: ' + self.available_locations[0] + '\n(as of ' + self.last_update + ')'
            self.Tweeter.Tweet(message)
        else:
            msg_bodies = []
            msg_body = ''
            for i in range(len(self.available_locations)):
                next_line = '\n' + self.available_locations[i]
                if len(msg_body + next_line) < 229:
                    msg_body = msg_body + next_line
                    continue
                msg_bodies.append(msg_body)
                msg_body = ''
            msg_bodies.append(msg_body)
            
            if len(msg_bodies) == 1:
                message = 'Available Locations: ' + msg_bodies[0] + '\n(as of ' + self.last_update + ')'
                self.Tweeter.tweet(message)
            else:
                first_msg = 'Available Locations: ' + msg_bodies[0] + '\n(as of ' + self.last_update + ')' + '\n(1/' + str(len(msg_bodies)) + ')'
                aux_bodies = msg_bodies[1:]
                self.Tweeter.tweet(first_msg)
                first_msg_id = self.Tweeter.last_tweet_id()
                for body in aux_bodies:
                    message = 'Available Locations: ' + body + '\n(as of ' + self.last_update + ')' + '\n('+str(msg_bodies.index(body)+1)+'/' + str(len(msg_bodies)) + ')'
                    self.Tweeter.reply(message, first_msg_id)

    def check_availability(self):
        self.old_available_locations = self.available_locations
        self.available_locations = []
        for loc in self.new_data:
            if self.new_data[loc] == 'Available':
                loc = loc.split(',')[0]
                self.available_locations.append(loc)
                if loc not in self.old_available_locations:
                    print(self.callsign + loc + ' Is Now ' + colored('AVAILABLE','green') + ' as of ' + self.new_update)
        for loc in self.old_available_locations:
            if loc not in self.available_locations:
                print(self.callsign + loc + ' Is Now ' + colored('UNAVAILABLE','green') + ' as of ' + self.new_update)
        
        
def run(event=None, context=None):
    running = True
    bot = CVSBot()
    while running:
        bot.update()
        time.sleep(3)
run()
