import math

# List of tuples
# 0: Name of the speed
# 1: Milliseconds between ticks of the clock
# 2: How many minutes pass with each tick
GAME_SPEEDS = [
    ('paused',math.inf,0),
    ('very slow', 1000, 1),
    ('slow', 100, 1),
    ('normal',10, 1),
    ('fast',1, 4),
    ('very fast', 1, 8)] 

# Background and text color
BG_COLOR = "lightblue1"
FG_COLOR = "black"


# You should modify this list of agent stats
# keys must be strings
# values should be lists
# The stats below are just examples to give you
# some inspiration. Come up with your own set
# based on the theme/setting you imagine.
STATS = {
    'location':['home','work','daycare','bar','park','jail'],
    'hungry':list(range(0,20)),
    'tired':list(range(0,5)),
    'bored':list(range(0,2)),
    'purpose':list(range(0,3)),
    'lonely':list(range(0,20)),
    'money':list(range(0,1000)),
    'dirty':list(range(0,5)),
    'sad':list(range(0,10)),
    'crazy':list(range(0,10)),
    'frustrated':list(range(0,10)),
    'lazy':list(range(0,10)),
    'confident':list(range(0,10)),
    'accomplished':list(range(0,10))
}

# Probably don't change this line.
STAT_NAMES = list(STATS.keys())

# Change if you want. I hope I don't get
# 40 submissions all about an agent named, Jimbo.
AGENT_NAME = 'Jimbo'
START_TIME = 1800 # 6:00 AM Monday
