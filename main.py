import time
from termcolor import colored
import datetime
from cvsrequests import CVSrequester
from twitterbot import Tweeter
from selfstate import SmallState


class CVSBot:
    def __init__(self):
        
        self.callsign = colored('[CVSBot]', 'magenta') + ': '
        self.TWEET_LINK = 'https://www.cvs.com/vaccine/intake/store/cvd-schedule.html?icid=coronavirus-lp-vaccine-sd-statetool'
        self.callsign = colored('[CVSBot]', 'magenta') + ': '
        self.requester = CVSrequester()
        self.Tweeter = Tweeter()
        self.small = SmallState()
        
        #Load saved state
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

    def update(self):
        
        #Print to console once every minute
        self.now = datetime.datetime.now().strftime("%I:%M %p")
        if self.now != self.then:
            print(self.callsign + 'Updating (' + self.now + ')')
        self.then = self.now
        
        # Get Location data
        self.new_data = self.requester.get_locations()
        self.check_availability()
        
        #Check for change in location data
        if self.available_locations != self.old_data and self.old_data != None:  # Change in data
            self.old_data = self.new_data
            if len(self.available_locations) == 0:
                print(self.callsign + colored('No Availability', 'red'))
            if len(self.available_locations) > 0:
                self.tweet_available_locations()
        
        time.sleep(2)

        #Get WR status
        self.waitingroom_status = self.requester.get_wr_status()

        #Check for change in WR status
        if self.waitingroom_status != self.old_waitingroom_status:
            self.tweet_waitingroom_status() 
        self.old_waitingroom_status = self.waitingroom_status
        self.small.update(self)
        
        time.sleep(2)
        
    def check_availability(self):
        self.old_available_locations = self.available_locations
        self.available_locations = list(self.new_data.keys())
        if self.available_locations != self.old_available_locations:
            for loc in self.available_locations:
                if loc not in self.old_available_locations:
                    print(self.callsign + loc + ' Is Now ' + colored('AVAILABLE','green') + ' as of ' + self.now)
                
            for loc in self.old_available_locations:
                if loc not in self.available_locations:
                    print(self.callsign + loc + ' Is Now ' + colored('UNAVAILABLE','red') + ' as of ' + self.now)
            if len(self.available_locations) > 0:
                self.tweet_available_locations()
                
    def tweet_waitingroom_status(self):
        if self.waitingroom_status == 'ENABLED':
            print(self.callsign + colored('Waiting Room Is Now ENABLED', 'red')+'(as of '+self.now+')')
            message = 'Waiting Room Is Now '+'ENABLED'+'\n(as of '+self.now+')'
            self.Tweeter.tweet(message)
        if self.waitingroom_status == 'DISABLED':
            print(self.callsign + colored('Waiting Room Is Now DISABLED', 'green'))
            message = 'Waiting Room Is Now DISABLED\n(as of '+self.now+')\n'+self.TWEET_LINK
            self.Tweeter.tweet(message)

    def tweet_available_locations(self):
        if len(self.available_locations) == 1:
            message = 'Available Location: ' + self.available_locations[0] +') \n(as of ' + self.now + ')' #'('+self.new_data[self.available_locations[0]]+')
            self.Tweeter.tweet(message)
        else:
            msg_bodies = []
            msg_body = ''
            for i in range(len(self.available_locations)):
                next_line = '\n- ' + self.available_locations[i] #+ ' ('+self.new_data[self.available_locations[i]]+')'
                if len(msg_body + next_line) < 229:
                    msg_body = msg_body + next_line
                    continue
                msg_bodies.append(msg_body)
                msg_body = ''
            msg_bodies.append(msg_body)
            
            if len(msg_bodies) == 1:
                message = 'Available Locations: ' + msg_bodies[0] + '\n(as of ' + self.now + ')'
                self.Tweeter.tweet(message)
            else:
                first_msg = 'Available Locations: ' + msg_bodies[0] + '\n(as of ' + self.now + ')' + '\n(1/' + str(len(msg_bodies)) + ')'
                aux_bodies = msg_bodies[1:]
                self.Tweeter.tweet(first_msg)
                first_msg_id = self.Tweeter.last_tweet_id()
                for body in aux_bodies:
                    message = 'Available Locations: ' + body + '\n(as of ' + self.now + ')' + '\n('+str(msg_bodies.index(body)+1)+'/' + str(len(msg_bodies)) + ')'
                    self.Tweeter.reply(message, first_msg_id)
        
def run():
    running = True
    bot = CVSBot()
    while running:
        bot.update()
run()
