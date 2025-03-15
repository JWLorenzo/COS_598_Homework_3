# COS 598_Homework_3
- Name: Jacob Lorenz
- Date: 2/24/25 - 3/?/25
- Assignment: 3
- Instructor: Dr. Hutchinson

# Writeup

My goal with this system was to simulate someone's daily life. I decided to use a Goal-Oriented Action Planning (GOAP) system to determine the actions with the least cost. From there, I created a weight system to make certain actions more desirable or undesirable at different times, effectively making them exclusive during specific periods. For example, Monday–Friday, there’s a work action that, if attempted outside the designated period, has infinite discontentment associated with it. But within the period, it has a value of 0, making it nearly exclusive.

After implementing GOAP, I expanded the system by adding automated biological modifiers that adjust stats to drive behavior. I also made the system easily scalable by tying all functionality to defs.py. Adding more behaviors is as simple as defining new actions, locations, or emotions. The system automatically accounts for them.

To refine decision-making, I added action requirements like location locking and time-of-day constraints. I also implemented a special "drive" action that tacks on a 30-minute time penalty and a 1 debt STAT penalty to move between locations. If an action isn’t valid at the current location, the system checks whether driving would make it viable. If so, it updates the best action accordingly.

I tried to keep the system as “hack”-free as possible by generalizing actions. The only hardcoded exceptions are for driving, paying fines, and sleeping. Those could have been generalized, but doing so would bloat the dictionary entries by instantiating more data structures within each value.

To make the experience feel more immersive, I included statuses and moods for the player. If stats exceed certain thresholds, they get statuses like "drunk," "broke," or "tired." Emotions work similarly but are semi-randomized, using a lambda function to determine the best-fitting mood based on the current state vector.

The biggest improvement I see right now is integrating other agents into the scene. I realized this would require significant reworking of hw3.py to handle multiple instantiated agents, so I opted to leave that out for now. If I were to implement it, I’d use a similar approach to locations and actions. If two agents are in the same location, actions exclusive to those agents would have the lowest discontentment, making them more likely to occur.

Observations:

The current agent weights lead to a lot of DUIs, which is… interesting behavior, to say the least.
I haven’t observed long sequences of idle time, so it seems like the weights are working well in the current implementation.


# Notes (pretty jumbled, but show the homework process)

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