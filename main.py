from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time
from termcolor import colored
import datetime
import os
import tweepy
import sys

class Tweeter:
    def __init__(self):
        API_KEY = 'API_KEY'
        API_SECRET = 'API_SECRET'
        ACCESS_TOKEN = 'ACCESS_TOKEN'
        ACCESS_SECRET = 'ACCESS_SECRET'
        
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        
        self.api = tweepy.API(auth)
        self.callsign = colored('[Tweeter]','cyan')+': '
        
    def tweet(self, tweet):
        try:
            self.api.update_status(tweet)
            print(self.callsign+'Tweeted: '+tweet)
            return True
        except tweepy.TweepError as e:
            print(self.callsign+e)
            return False
        
    def last_tweet_id(self):
        return self.api.user_timeline()[0].id
    
    def last_tweet_text(self):
        return self.api.user_timeline()[0].text
        
        
class CVSBot:
    def __init__(self):
        self.callsign = colored('[CVSBot]','magenta')+': '
        print(self.callsign+'Initializing Bot')
        self.CVS_URL = 'https://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-link2-coronavirus-vaccine#'
        self.TWEET_LINK = 'https://www.cvs.com/vaccine/intake/store/cvd-schedule.html?icid=coronavirus-lp-vaccine-sd-statetool'
        self.MASS_BUTTON_XPATH = '//*[@id="empty-0d710bd9ab"]/content/div/div/div/div[3]/div/div/div[2]/div/div[5]/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div/div/div/div[2]/ul/li[2]'
        self.UPDATE_TS_XPATH = '//*[@id="vaccineinfo-MA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[5]/div'
        self.CITIES_XPATH = '//*[@id="vaccineinfo-MA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table/tbody/tr/td[1]'
        self.STATUSES_XPATH = '//*[@id="vaccineinfo-MA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table/tbody/tr/td[2]'
        self.FEEDBACK_BUTTON_XPATH = '//*[@id="acsMainInvite"]/div/a[1]'
        self.callsign = colored('[CVSBot]','magenta')+': '
        saved_state = self.get_saved_state()
        if saved_state:
            self.last_update = self.saved_state.last_update
            self.old_data = self.saved_state.old_data
            self.then = self.saved_state.then
            self.available_locations = self.saved_state.available_locations
        else:
            self.last_update = None
            self.old_data = None
            self.then = None
            self.available_locations = []
        self.Tweeter = Tweeter()
        self.driver = webdriver.Chrome() 
        self.driver.set_window_position(-2000,0)
        self.driver.get(self.CVS_URL)
        print(self.callsign+'Initialized')
        
    def update(self):
        self.now = datetime.datetime.now().strftime("%I:%M %p")
        if self.now != self.then:
            print(self.callsign+'Updating ('+self.now+')')
        self.then = self.now
        sys.stdout.flush()
        try:
            self.driver.find_element_by_xpath(self.MASS_BUTTON_XPATH).click()
        except ElementClickInterceptedException: # Deal with feedback box
            self.driver.find_element_by_xpath(self.FEEDBACK_BUTTON_XPATH).click()
            self.driver.find_element_by_xpath(self.MASS_BUTTON_XPATH).click()
        time.sleep(1)
        
        #Check Timestamp of Last update
        self.new_update = self.driver.find_element_by_xpath(self.UPDATE_TS_XPATH).text.split('.')[0][13:]
        if self.new_update != self.last_update: #Found update, Initial path
            self.last_update = self.new_update
            print(self.callsign+colored('Found New Update @'+self.last_update, 'yellow'))
            print(self.callsign+colored('Checking For Availability', 'yellow'))
        
            self.cities  = list(map(lambda el: el.text, self.driver.find_elements_by_xpath(self.CITIES_XPATH)))
            self.statuses = list(map(lambda el: el.text, self.driver.find_elements_by_xpath(self.STATUSES_XPATH)))
            self.new_data = dict(zip(self.cities, self.statuses))
            self.check_availability()
            if self.new_data == self.old_data: #No change in data
                print(self.callsign+colored('No Change In Availability', 'red'))
            
            if self.new_data != self.old_data: #Change in data
                self.old_data = self.new_data
                if len(self.available_locations) == 0:
                    print(self.callsign+colored('No Availability', 'red'))
            if len(self.available_locations) > 0:
                self.tweet_available_locations()
                

    def tweet_available_locations(self):
        if len(self.available_locations) <= 8:
            message = 'Available location(s): '+",".join(self.available_locations)+' (as of '+self.last_update+'); '+self.TWEET_LINK
        if len(self.available_locations) > 8:   
            message = '('+str(len(self.available_locations))+')'+'Available locations (as of '+self.last_update+'); '+self.TWEET_LINK
        tweet_success = self.Tweeter.tweet(message)
        if tweet_success:
            curr_tweet = self.Tweeter.last_tweet_id()
            self.tweets[curr_tweet] = self.available_locations.copy()

    def check_availability(self):
        self.old_available_locations = self.available_locations
        self.available_locations = []
        for i in self.new_data:
            if self.new_data[i] == 'Available':
                self.available_locations.append(i)
                if i not in self.old_available_locations:
                    print(self.callsign+i+'Is Now '+colored('AVAILABLE','green')+' as of '+self.new_update)
        for i in self.old_available_locations:
            if i not in self.available_locations:
                print(self.callsign+i+'Is Now '+colored('UNAVAILABLE','green')+' as of '+self.new_update)
        
def run(event=None, context=None):
    running = True
    bot = CVSBot()
    while running:  
        bot.update()
        time.sleep(3)
        bot.driver.refresh()
run()
