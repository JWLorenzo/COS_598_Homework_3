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