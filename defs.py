import math
import numpy as np
import ztime

# List of tuples
# 0: Name of the speed
# 1: Milliseconds between ticks of the clock
# 2: How many minutes pass with each tick
GAME_SPEEDS = [
    ("paused", math.inf, 0),
    ("very slow", 1000, 1),
    ("slow", 100, 1),
    ("normal", 10, 1),
    ("fast", 1, 4),
    ("very fast", 1, 8),
]

# Emotion system

EMOTION_VECTORS = {
    # neutral
    "ambivalent": [np.array([0, 0]), None],
    # Positive
    "joyful": [np.array([1.0, 1.0]), True],
    "trusting": [np.array([0.0, 2.0]), True],
    "surprised": [np.array([-2.0, 1.0]), True],
    "anticipating": [np.array([2.0, 0.5]), True],
    "grateful": [np.array([1.0, 1.5]), True],
    "hopeful": [np.array([1.5, 1.0]), True],
    "content": [np.array([0.5, 0.5]), True],
    "proud": [np.array([2.0, 2.0]), True],
    "amused": [np.array([1.0, 0.5]), True],
    "curious": [np.array([1.5, -0.5]), True],
    # Negative Emotions
    "sad": [np.array([-1.0, -1.0]), False],
    "disgusted": [np.array([0.0, -2.0]), False],
    "angered": [np.array([1.5, -1.5]), False],
    "fearful": [np.array([-1.5, 1.5]), False],
    "jealous": [np.array([1.0, -2.0]), False],
    "guilty": [np.array([-1.5, -0.5]), False],
    "ashamed": [np.array([-1.0, -1.5]), False],
    "stressed": [np.array([2.0, -1.0]), False],
    "lonely": [np.array([-2.0, -1.5]), False],
    "bored": [np.array([-0.5, 0.0]), False],
}

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
    "location": [
        ["home", "work", "bar", "park", "jail", "arcade", "restaurant", "doctor"],
    ],
    "hunger": [list(range(0, 20)), "hungry"],
    "thirst": [list(range(0, 20)), "thirsty"],
    "sleep": [list(range(0, 8)), "tired"],
    "recreation": [list(range(0, 20)), "bored"],
    "motivation": [list(range(0, 10)), "burnt-out"],
    "social": [list(range(0, 20)), "solitary"],
    "debt": [list(range(0, 40)), "broke"],
    "hygiene": [list(range(0, 20)), "dirty"],
    "bladder": [list(range(0, 20)), "gotta go #1"],
    "colon": [list(range(0, 20)), "gotta go #2"],
    "blood alcohol": [list(range(0, 10)), "drunk"],
    "caffeine": [list(range(0, 10)), "jittery"],
}


# Breakdown of an action: "name": {[location(s)], {stats affected}, time, [halted stats during action], [[preferred hours],[preferred days],(mult outside times,mult inside times)]}
""" "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday","""
ACTIONS = {
    "driving": [
        ["anywhere"],
        {"debt": 1},
        30,
        [],
        [
            [],
            [],
            (),
        ],
    ],
    "walking": [
        ["park"],
        {"sleep": 1, "social": -2},
        60,
        [],
        [
            [],
            [],
            (),
        ],
    ],
    "idle": [
        ["anywhere"],
        {},
        10,
        [],
        [
            [],
            [],
            (),
        ],
    ],
    "eating at work": [
        ["work"],
        {"hunger": -4, "colon": 2},
        30,
        ["hunger", "recreation"],
        [
            [12],
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
            ],
            (math.inf, 0.01),
        ],
    ],
    "drinking water at work": [
        ["work"],
        {"thirst": -5, "bladder": 2, "social": -1},
        10,
        ["thirst", "recreation"],
        [
            [7, 8, 9, 10, 11, 13, 14, 15, 16],
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
            ],
            (math.inf, 0.01),
        ],
    ],
    "eating dinner": [
        ["home", "bar", "jail"],
        {"hunger": -5, "colon": 2, "debt": 1},
        30,
        ["hunger", "recreation"],
        [
            [17, 18, 19, 20, 21, 22],
            [],
            (1.5, 1),
        ],
    ],
    "drinking water": [
        ["home", "work", "bar", "restaurant", "park", "jail"],
        {"thirst": -2, "bladder": 2},
        10,
        ["thirst", "recreation"],
        [
            [],
            [
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ],
            (1, 1),
        ],
    ],
    "drinking beer": [
        ["bar"],
        {
            "thirst": -4,
            "hunger": -1,
            "bladder": 2,
            "colon": 1,
            "motivation": -1,
            "debt": 1,
            "blood alcohol": 4,
        },
        10,
        ["thirst", "recreation", "motivation"],
        [
            [17, 18, 19, 20, 21],
            [],
            (2, 0.8),
        ],
    ],
    "drinking coffee": [
        ["home", "work"],
        {
            "thirst": -4,
            "bladder": 3,
            "motivation": -2,
            "debt": 1,
            "sleep": -1,
            "caffeine": 4,
        },
        10,
        ["thirst", "sleep"],
        [
            [6, 7, 8, 9, 10, 11],
            [],
            (1.5, 1),
        ],
    ],
    "sleeping": [
        ["home", "jail"],
        {
            "sleep": -8,
            "colon": 2,
            "bladder": 2,
            "hunger": 1,
            "thirst": 1,
        },
        480,
        ["sleep", "hunger", "recreation", "motivation", "social"],
        [
            [
                22,
                23,
            ],
            [],
            (math.inf, 0),
        ],
    ],
    "going bathroom 1": [
        ["home", "jail", "restaurant", "bar", "work"],
        {"bladder": -5},
        6,
        [],
        [
            [],
            [
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ],
            (1, 1),
        ],
    ],
    "going bathroom 2": [
        ["home", "jail", "restaurant", "bar", "work"],
        {"colon": -5},
        8,
        [],
        [
            [],
            [
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ],
            (1, 1),
        ],
    ],
    "texting": [
        ["anywhere"],
        {"social": -1},
        5,
        [],
        [
            [],
            [],
            (),
        ],
    ],
    "therapy": [
        ["doctor"],
        {"motivation": -1, "debt": 2, "social": -1},
        60,
        ["motivation", "social"],
        [
            [17, 18],
            ["Monday"],
            (math.inf, 0),
        ],
    ],
    "going bathroom 3": [
        ["home", "jail", "restaurant", "bar", "work"],
        {"colon": -5, "bladder": -5, "hygiene": 1},
        10,
        [],
        [
            [],
            [
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ],
            (1, 1),
        ],
    ],
    "playing a video game": [
        ["arcade"],
        {"recreation": -3},
        60,
        ["recreation"],
        [
            [17, 18, 19, 20, 21, 22],
            [],
            (math.inf, 1),
        ],
    ],
    "eating a fine meal": [
        ["restaurant"],
        {"hunger": -3, "motivation": -1, "debt": 2, "colon": 1},
        2,
        ["recreation"],
        [
            [17, 18, 19, 20, 21, 22],
            [],
            (math.inf, 1),
        ],
    ],
    "playing a board game": [
        ["home", "jail"],
        {"recreation": -2},
        90,
        ["recreation"],
        [
            [17, 18, 19, 20, 21, 22],
            [],
            (math.inf, 1),
        ],
    ],
    "playing darts": [
        ["bar"],
        {"recreation": -2, "social": -1},
        20,
        ["recreation"],
        [
            [17, 18, 19, 20, 21, 22],
            [],
            (math.inf, 1),
        ],
    ],
    "taking a shower": [
        ["home", "jail"],
        {"hygiene": -4},
        10,
        ["hygiene"],
        [
            [6, 7, 20, 21, 22],
            [],
            (math.inf, 1),
        ],
    ],
    "brushing teeth": [
        ["home", "jail"],
        {"hygiene": -2},
        2,
        ["hygiene"],
        [
            [6, 7, 20, 21, 22],
            [],
            (math.inf, 1),
        ],
    ],
    "washing hands": [
        ["home", "jail"],
        {"hygiene": -1},
        1,
        ["hygiene"],
        [
            [],
            [
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ],
            (math.inf, 1),
        ],
    ],
    "programming at work": [
        ["work"],
        {
            "debt": -2,
        },
        60,
        ["social", "recreation"],
        [
            [7, 8, 9, 10, 11, 13, 14, 15, 16],
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
            ],
            (math.inf, 0),
        ],
    ],
    "programming at home": [
        ["home"],
        {"recreation": -1},
        60,
        ["recreation"],
        [
            [17, 18, 19, 20, 21, 22],
            [],
            (1.5, 1),
        ],
    ],
    "watching tv": [
        ["home"],
        {"recreation": -2},
        60,
        ["recreation"],
        [
            [],
            ["Saturday", "Sunday"],
            (math.inf, 1),
        ],
    ],
    "feeding the ducks": [
        ["park"],
        {"recreation": -1, "social": -1},
        60,
        ["recreation"],
        [
            [],
            ["Saturday", "Sunday"],
            (math.inf, 1),
        ],
    ],
    "watching cat videos": [
        ["anywhere"],
        {
            "motivation": -1,
        },
        5,
        ["recreation"],
        [
            [],
            [],
            (),
        ],
    ],
    "pay fine": [
        ["jail"],
        {
            "motivation": 1,
            "debt": 5,
        },
        45,
        [],
        [
            list(range(6, 12)),
            [],
            (math.inf, 0.7),
        ],
    ],
}

BIO_STATS = [
    "hunger",
    "thirst",
    "sleep",
    "recreation",
    "motivation",
    "social",
    "hygiene",
    "blood alcohol",
    "caffeine",
]


# Probably don't change this line.
STAT_NAMES = list(STATS.keys())

# Change if you want. I hope I don't get
# 40 submissions all about an agent named, Jimbo.
START_TIME = 1800  # 6:00 AM Monday
