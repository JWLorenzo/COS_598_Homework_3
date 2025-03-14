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
    "joy": np.array([1, 1]),
    "trust": np.array([0, 2]),
    "fear": np.array([-1, 1]),
    "surprise": np.array([-2, 0]),
    "sadness": np.array([-1, -1]),
    "disgust": np.array([0, -2]),
    "anger": np.array([1, -1]),
    "anticipation": np.array([2, 0]),
}

# This is not an exhaustive list because emotion is too complex to capture in vector form

complex_emotions = {
    "in love": EMOTION_VECTORS["joy"] + EMOTION_VECTORS["trust"],
    "submissive": EMOTION_VECTORS["trust"] + EMOTION_VECTORS["fear"],
    "in awe": EMOTION_VECTORS["fear"] + EMOTION_VECTORS["surprise"],
    "disapproving": EMOTION_VECTORS["surprise"] + EMOTION_VECTORS["sadness"],
    "remorseful": EMOTION_VECTORS["sadness"] + EMOTION_VECTORS["disgust"],
    "contemptuous": EMOTION_VECTORS["disgust"] + EMOTION_VECTORS["anger"],
    "aggressive": EMOTION_VECTORS["anticipation"] + EMOTION_VECTORS["anger"],
    "optimistic": EMOTION_VECTORS["anticipation"] + EMOTION_VECTORS["joy"],
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
        "home",
        "work",
        "bar",
        "park",
        "jail",
        "arcade",
        "restaurant",
    ],
    "hunger": list(range(0, 20)),
    "thirst": list(range(0, 20)),
    "sleep": list(range(0, 8)),
    "recreation": list(range(0, 10)),
    "motivation": list(range(0, 3)),
    "social": list(range(0, 20)),
    "debt": list(range(0, 1000)),
    "hygiene": list(range(0, 5)),
    "bathroom_no_1": list(range(0, 20)),
    "bathroom_no_2": list(range(0, 20)),
}

STATUSES = {
    "statuses": ["hungry", "tired", "dirty", "burnt-out", "drunk"],
    "mood": [
        "ambivalent",
        "in love",
        "submissive",
        "in awe",
        "disapproving",
        "remorseful",
        "contemptuous",
        "aggressive",
        "optimistic",
    ],
    "joy": list(range(0, 20)),
    "trust": list(range(0, 20)),
    "fear": list(range(0, 20)),
    "surprise": list(range(0, 20)),
    "sadness": list(range(0, 20)),
    "disgust": list(range(0, 20)),
    "anger": list(range(0, 20)),
    "anticipation": list(range(0, 20)),
}


# Breakdown of an action: "name": {[location(s)], {stats affected}, time, [halted stats during action], [[preferred hours],[preferred days],(mult outside times,mult inside times)]}
"""                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday","""
ACTIONS = {
    "drive": [
        ["anywhere"],
        {},
        30,
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
        0,
        [],
        [
            [],
            [],
            (),
        ],
    ],
    "eat_work": [
        ["work"],
        {"hunger": -2, "bathroom_no_2": 2},
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
            (math.inf, 0.9),
        ],
    ],
    "eat_dinner": [
        ["home", "bar", "restaurant", "jail"],
        {"hunger": -3, "bathroom_no_2": 2},
        30,
        ["hunger", "recreation"],
        [
            [17, 18, 19, 20, 21, 22],
            [],
            (1.5, 1),
        ],
    ],
    "drink_water": [
        ["home", "work", "bar", "restaurant", "park", "jail"],
        {"thirst": -2, "bathroom_no_1": 2},
        10,
        ["thirst", "recreation"],
        [
            [],
            [],
            (),
        ],
    ],
    "drink_beer": [
        ["home", "bar"],
        {
            "thirst": -2,
            "hunger": -1,
            "bathroom_no_1": 2,
            "bathroom_no_2": 1,
            "motivation": -1,
            "debt": 3,
        },
        10,
        ["thirst", "recreation", "motivation"],
        [
            [17, 18, 19, 20, 21, 22],
            [],
            (1.5, 1),
        ],
    ],
    "drink_coffee": [
        ["home", "work"],
        {
            "thirst": -2,
            "bathroom_no_1": 3,
            "motivation": -2,
            "debt": 1,
            "sleep": -1,
        },
        10,
        ["thirst", "sleep"],
        [
            [],
            [],
            (),
        ],
    ],
    "sleep": [
        ["home", "jail"],
        {
            "sleep": -8,
            "bathroom_no_2": 2,
            "bathroom_no_1": 2,
            "hunger": 1,
            "thirst": 1,
            "hygiene": 3,
        },
        480,
        ["sleep", "hunger", "recreation"],
        [
            [22, 23, 24, 0, 1],
            [],
            (math.inf, 1),
        ],
    ],
    "bathroom_1": [
        ["home", "jail", "restaurant", "work"],
        {"bathroom_no_1": -5},
        6,
        [],
        [
            [],
            [],
            (),
        ],
    ],
    "bathroom_2": [
        ["home", "jail", "restaurant", "work"],
        {"bathroom_no_2": -5},
        8,
        [],
        [
            [],
            [],
            (),
        ],
    ],
    "bathroom_3": [
        ["home", "jail", "restaurant", "work"],
        {"bathroom_no_2": -5, "bathroom_no_1": -5, "hygiene": 1},
        10,
        [],
        [
            [],
            [],
            (),
        ],
    ],
    "video_game": [
        ["arcade"],
        {"recreation": -3},
        60,
        ["recreation"],
        [
            [17, 18, 19, 20, 21, 22],
            [],
            (1, 1),
        ],
    ],
    "board_game": [
        ["home", "jail"],
        {"recreation": -2},
        90,
        ["recreation"],
        [
            [],
            [],
            (),
        ],
    ],
    "darts": [
        ["bar"],
        {"recreation": -2, "social": -1},
        20,
        ["recreation"],
        [
            [17, 18, 19, 20, 21, 22],
            [],
            (1.5, 1),
        ],
    ],
    "shower": [
        ["home", "jail"],
        {"hygiene": -2},
        10,
        ["hygiene"],
        [
            [6, 7, 20, 21, 22],
            [],
            (math.inf, 0.9),
        ],
    ],
    "brush_teeth": [
        ["home", "jail"],
        {"hygiene": -1},
        2,
        ["hygiene"],
        [
            [6, 7, 20, 21, 22],
            [],
            (math.inf, 0.9),
        ],
    ],
    "program (work)": [
        ["work"],
        {"debt": -2},
        60,
        [],
        [
            [8, 9, 10, 11, 13, 14, 15, 16],
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
            ],
            (math.inf, 0.9),
        ],
    ],
    "program (fun)": [
        ["home"],
        {"recreation": -1},
        60,
        ["recreation"],
        [
            [],
            [],
            (),
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
]


# Probably don't change this line.
STAT_NAMES = list(STATS.keys())

# Change if you want. I hope I don't get
# 40 submissions all about an agent named, Jimbo.
AGENT_NAME = "obmiJ"
START_TIME = 1800  # 6:00 AM Monday
