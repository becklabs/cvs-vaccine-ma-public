import dill

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