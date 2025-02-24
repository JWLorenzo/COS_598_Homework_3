import math
import ztime

class Action:
    def __init__(self, msg, start_time, end_time):
        self.msg = msg
        self.start_time = start_time  # Time object
        self.end_time = end_time      # Time object
    def is_running(self, cur_time):
        return cur_time < self.end_time
    def is_done(self, cur_time):
        return cur_time >= self.end_time
    def get_msg(self):
        return self.msg

