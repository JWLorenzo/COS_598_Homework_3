import action

class Agent:
    def __init__(self, name, stats,
                 idle_message="Idle",
                 action=None):
        self.name = name
        self.stats = stats
        self.idle_message = idle_message
        self.action = action
    def get_stat(self, stat_name):
        return self.stats[stat_name]
    def change_stat(self, stat_name, amt):
        stat = self.stats[stat_name]
        stat.change_index(amt)
    def get_name(self):
        return self.name
    def get_action(self):
        return self.action
    def set_action(self, action):
        self.action = action
    def update_action(self, cur_time):
        if self.action is not None:
            if self.action.is_done(cur_time):
                self.action = None
    def is_idle(self):
        return self.action is None
    def get_idle_message(self):
        return self.idle_message
    def get_action_message(self):
        if self.is_idle():
            return self.idle_message
        else:
            return self.action.get_msg()
        
