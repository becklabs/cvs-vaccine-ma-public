from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time
from termcolor import colored
import datetime
import os
from twilio.rest import Client
import tweepy

class Tweeter:
    def __init__(self):
        API_KEY = 'API_KEY'
        API_SECRET = 'API_SECRET'
        ACCESS_TOKEN = 'ACCESS_TOKEN'
        ACCESS_SECRET = 'ACCESS_SECRET'
        
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        
        self.api = tweepy.API(auth)
    
    def tweet(self, tweet):
        try:
            self.api.update_status(tweet)
            print(colored('[Tweeter]: ','cyan')+' Tweeted: '+tweet)
            return True
        except tweepy.TweepError as e:
            print(e)
            return False
        
    def last_tweet_id(self):
        return self.api.user_timeline()[0].id
    
    def last_tweet_text(self):
        return self.api.user_timeline()[0].text
    
    def reply(self, message, tweet_id):
        self.api.update_status(status = message, 
                                in_reply_to_status_id = tweet_id, 
                                auto_populate_reply_metadata=True)
        print(colored('[Tweeter]','cyan')+': Replied: '+message)
        
class SMS:
    def __init__(self):
        account_sid = 'SID'
        auth_token = 'AUTH_TOKEN'
        self.client = Client(account_sid, auth_token)
    
    def send(self, message, reciever):
        self.client.api.account.messages.create(
            to=reciever,
            from_="+SENDER",
            body=message)
        
class CVSBot:
    def __init__(self):
        self.CVS_URL = "https://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-link2-coronavirus-vaccine#"
        self.MASS_BUTTON_XPATH = '//*[@id="empty-0d710bd9ab"]/content/div/div/div/div[3]/div/div/div[2]/div/div[5]/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div/div/div/div[2]/ul/li[2]'
        self.UPDATE_TS_XPATH = '//*[@id="vaccineinfo-MA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[5]/div'
        self.CITIES_XPATH = '//*[@id="vaccineinfo-MA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table/tbody/tr/td[1]'
        self.STATUSES_XPATH = '//*[@id="vaccineinfo-MA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table/tbody/tr/td[2]'
        self.FEEDBACK_BUTTON_XPATH = '//*[@id="acsMainInvite"]/div/a[1]'
        self.last_update = None
        self.driver = webdriver.Chrome() 
        self.driver.set_window_position(-2000,0)
        self.driver.get(self.CVS_URL)
        self.SMS = SMS()
        self.Tweeter = Tweeter()
        self.initial = True
        self.tweets = {}
        self.data = {}
    def update(self):
        if not self.initial:
                self.driver.refresh()
        self.initial = False
        
        try:
            click_massachusetts = self.driver.find_element_by_xpath(self.MASS_BUTTON_XPATH).click()
            
        except ElementClickInterceptedException:
            feedback_survey = self.driver.find_element_by_xpath(self.FEEDBACK_BUTTON_XPATH).click()
            click_massachusetts = self.driver.find_element_by_xpath(self.MASS_BUTTON_XPATH).click()
            
        last_update = self.driver.find_element_by_xpath(self.UPDATE_TS_XPATH).text.split('.')[0][13:]
        if self.last_update == last_update:
            self.new_update = False
            self.last_update = last_update
            return
        else:
            self.new_update = True
            self.last_update = last_update
            print('CVS updated @ '+self.last_update)
            cities  = list(map(lambda el: el.text, self.driver.find_elements_by_xpath(self.CITIES_XPATH)))
            statuses = list(map(lambda el: el.text, self.driver.find_elements_by_xpath(self.STATUSES_XPATH)))
            data = dict(zip(cities, statuses))
            if self.data == data:
                self.new_data = False
            else:
                self.data = data
                self.new_data = True
                print('New Data')
            
    def print_pretty_data(self):
        clear = lambda: os.system('cls')
        clear()
        middle_ind = len(self.data)//2
        column1 = list(zip(list(self.data.keys())[:middle_ind], list(self.data.values())[:middle_ind]))
        column2 = list(zip(list(self.data.keys())[middle_ind:], list(self.data.values())[middle_ind:]))
        tail = ''
        if len(column1) > len(column2):
            tail = column1[-1]
            print(tail)
            column1.remove(tail)
        if len(column2) > len(column1):
            tail = column2[-1]
            column2.remove(tail)
        for row in range(len(column1)):
            c1_color = 'green'
            c2_color = 'green'
            tail_color = 'green'
            if column1[row][1] == 'Fully Booked':
                c1_color = 'red'
            if column2[row][1] == 'Fully Booked':
                c2_color = 'red'
            print(column1[row][0]+': '+colored(column1[row][1], c1_color)+' '*(39-len(column1[row][0]+': '+column1[row][1]))+column2[row][0]+': '+colored(column2[row][1], c2_color))
        if tail != '':
            if tail[1] == 'Fully Booked':
                tail_color = 'red'
            print(' '*39+tail[0]+': '+colored(tail[1], tail_color))

    def text_available_locations(self, reciever):
        if len(self.available_locations) != 0:
            self.SMS.send(message = 'Available location(s): '+str(self.available_locations)+' (as of '+self.last_update+')',
                              reciever = reciever)

    def tweet_available_locations(self):
        if len(self.available_locations) != 0:
            message = 'Available location(s): '+str(self.available_locations)+' (as of '+self.last_update+'); https://www.cvs.com/vaccine/intake/store/cvd-schedule.html?icid=coronavirus-lp-vaccine-sd-statetool'
        if len(self.available_locations) > 15:   
            message = 'Available location(s): '+str(self.available_locations[:10])+' and others '+ '(as of '+self.last_update+'); https://www.cvs.com/vaccine/intake/store/cvd-schedule.html?icid=coronavirus-lp-vaccine-sd-statetool'
            if message == self.Tweeter.last_tweet_text():
                return
            tweet_success = self.Tweeter.tweet(message)
            if tweet_success:
                curr_tweet = self.Tweeter.last_tweet_id()
                self.tweets[curr_tweet] = self.available_locations.copy()
            
    def update_tweets(self):
        removals = []
        for tweet_id in self.tweets:
            for loc in self.tweets[tweet_id]:
                if loc not in self.available_locations:  
                    self.Tweeter.reply(loc+' is now UNAVAILABLE (as of '+self.last_update+')', tweet_id)
                    self.tweets[tweet_id].remove(loc)
            if len(self.tweets[tweet_id]) == 0:
                removals.append(tweet_id)
        for tweet_id in removals:
            self.tweets.pop(tweet_id)
            
    def check_availability(self):
        self.available_locations = []
        for i in self.data:
            if self.data[i] == 'Available':
                self.available_locations.append(i)

bot = CVSBot()
while True:  
    bot.update()
    if bot.new_update:
        bot.check_availability()
        bot.tweet_available_locations()
        #bot.update_tweets()
        if bot.new_data:
            bot.print_pretty_data()
    time.sleep(3)
