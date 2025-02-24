import math

class Time:
    MINS_IN_HOUR = 60
    HOURS_IN_DAY = 24
    DAYS_IN_WEEK = 7
    DAYS_OF_WEEK = [
        'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday']
    def __init__(self, minute):
        self.minute = minute
    def __lt__(self, o):
        return self.minute < o.minute
    def __eq__(self, o):
        return self.minute == o.minute
    def __ge__(self, o):
        return self.minute >= o.minute
    def __add__(self, o):
        return Time(self.minute + o.minute)
    def __str__(self):
        return f"{self.day_of_week()} {self.hour():02}:{self.minit():02}"
    def minit(self):
        _min = self.minute % self.MINS_IN_HOUR
        return _min
    def hour(self):
        hour = (self.minute // self.MINS_IN_HOUR) % self.HOURS_IN_DAY
        return hour
    def day(self):
        day = (self.minute // (self.MINS_IN_HOUR*self.HOURS_IN_DAY)) % self.DAYS_IN_WEEK
        return day
    def day_of_week(self):
        return self.DAYS_OF_WEEK[self.day()]
    def tick(self, amt):
        self.minute += amt

def infinity():
    return Time(math.inf)
