# COS 598_Homework_3
- Name: Jacob Lorenz
- Date: 2/24/25 - 3/?/25
- Assignment: 3
- Instructor: Dr. Hutchinson

# Notes
- Instantiating agent objects
    - If two agents are in the same area, have a social interaction
        - Could be positive or negative   

- Files I'm expected to futz around with:
    - defs.py
    - decision.py
- Files I probably don't need to futz with:
    - agent_stat.py
    - ztime.py
    - hw3.py
    - agent.py

- Plans for the assignment:
    - Stat system
        - STR, DEX, CON, INT, WIS, CHA
        - Hunger, Thirst, Sleep, Mood, Recreation, Money
        - Lower mood unlocks new activities such as seeing a therapist
    - Traits
        - Good sport: get mood bonus from gaming regardless of win/loss
        - Competitive: Winning grants major mood bonus
        - Sore Loser: Losing grants major negative mood penalty
        - Introvert: Less likely to have social interactions occur
            - More likely to do activities that have low social interaction
        - Extrovert: More likely to have social interactions occur
            - More likely to do activities that have high social interaction
        - Can be temporary traits:
            - Drunk: Increases social interaction
            - Depressed
            - Tired
            - Hungry
            - Bored
    - Locations
        - Activities at location
        - Social interaction if two agents are at the same location
            - Can be positive or negative based on stats and result of activity
    - Relations
        - Opinion of other agents affects willingness to have social interaction occur.

    - Mood is a multi axis calculation:
        - We could make mood a vector-based system


    - Breakdown of how actions are going to work:
        Actions are going to be a list of lists

        We can also check if it's a social interaction action or not: e.g. you can't play ping pong by yourself

        We can also have actions that can only be done with certain members: e.g. you can go play video games with Bob, but Steve doesn't play video games
        
        Action{location(can be a list or just one), modifies(list of how it affects every value), time}


    - Actions have different weights at different times of day

    - Check if path from one location to another location is desirable for a given action

    - Once / day actions?

    - Do we want high values to be better or worse?
        - Worse because we start at 0 in everything

    - We should add a multiplier for time

    - We also need to normalize the values

    Typical Schedule:

    Mon: wake up 6:00am, work(8am - 12pm, 1pm-5pm), other: 5pm-10:30
    Tue: wake up 6:00am, work(8am - 12pm, 1pm-5pm), other: 5pm-10:30
    Wed: wake up 6:00am, work(8am - 12pm, 1pm-5pm), other: 5pm-10:30
    Thur: wake up 6:00am, work(8am - 12pm, 1pm-5pm), other: 5pm-10:30
    Fri: wake up 6:00am, work(8am - 12pm, 1pm-5pm), other: 5pm-10:30
    Sat: wake up 9:00am, other: 9am - 1am
    Sun: wake up 9:00am, other: 9am - 1am



Objectives:

Set up semi random hunger / thirst over the day

Set up weighted activities at given times

Set up activities that are time related

Normalize the weights of activities

Instantiate multiple agents