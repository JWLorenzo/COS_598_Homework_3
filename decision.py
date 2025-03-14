import enum
import ztime
import action
from defs import STATS, ACTIONS, BIO_STATS
import agent
import math

## Make sure to remove this
import random


def getDiscontentment(value: float) -> float:
    return value * value


def discontentment(
    myagent: agent.Agent, action: list[list, dict, ztime.Time], goals: dict
) -> float:
    goal_List = list(goals.keys())[1:]
    discontentment_Value = 0

    for goal in goal_List:
        new_Value = 1 + max(
            0, myagent.get_stat(goal).get_value() + action[1].get(goal, 0)
        ) / (len(myagent.get_stat(goal).values) - 1)
        discontentment_Value += getDiscontentment(new_Value)
    return discontentment_Value


def make_decisionsys(
    myagent: agent.Agent, actions: dict, goals: dict, curtime: ztime.Time
) -> action.Action:
    best_Action = "idle"
    best_Value = math.inf

    for _action in list(actions.keys())[1:]:

        this_Value = discontentment(myagent, actions.get(_action), goals)
        if len(actions.get(_action)[4][0]) or len(actions.get(_action)[4][1]):
            if (
                (len(actions.get(_action)[4][0]) == 0)
                or (curtime.hour() in actions.get(_action)[4][0])
            ) and (
                (len(actions.get(_action)[4][1]) == 0)
                or (curtime.day_of_week() in actions.get(_action)[4][1])
            ):
                this_Value *= actions.get(_action)[4][2][1]
            else:
                this_Value *= actions.get(_action)[4][2][0]
        if (myagent.get_stat("location").get_value() in actions.get(_action)[0]) or (
            "anywhere" in actions.get(_action)[0]
        ):
            if this_Value < best_Value:
                best_Value = this_Value
                best_Action = _action
        else:
            print("check if driving better")
            this_Value += discontentment(myagent, actions.get("drive"), goals)
            if this_Value < best_Value:
                best_Value = this_Value
                best_Action = "driving"
                print("driving worth")

    time_modifier = ztime.Time(actions.get(best_Action)[2])
    chosen_Action = action.Action(best_Action, curtime, curtime.__add__(time_modifier))

    return chosen_Action


def bio_needs(myagent: agent.Agent, curtime: ztime.Time):
    if (
        (curtime.hour() % 2 == 0)
        and (curtime.minit() == 0)
        and (myagent.last_bio != curtime.hour())
    ):
        for stat in BIO_STATS:
            if myagent.action != None:
                if stat not in ACTIONS.get(myagent.action.get_msg())[3]:
                    myagent.change_stat(stat, 1)

            else:
                myagent.change_stat(stat, 1)
        myagent.last_bio = curtime.hour()


def update_stats(myagent: agent.Agent) -> None:
    if myagent.last_action != None and myagent.last_action.get_msg() != "idle":
        if myagent.last_action.get_msg() == "driving":
            myagent(
                "location",
                abs(
                    STATS.get("location").index(myagent.location)
                    - STATS.get("location").index(
                        STATS.get_stat("location").get_value()
                    )
                ),
            )
        for stat in list(STATS.keys())[1:]:
            calculated_total = myagent.get_stat(stat).get_value() + ACTIONS.get(
                myagent.last_action.get_msg()
            )[1].get(stat, 0)
            if calculated_total >= 0 and calculated_total < len(
                myagent.get_stat(stat).values
            ):
                myagent.change_stat(
                    stat, ACTIONS.get(myagent.last_action.get_msg())[1].get(stat, 0)
                )
            else:
                if calculated_total < len(myagent.get_stat(stat).values):
                    myagent.change_stat(stat, -myagent.get_stat(stat).get_value())
                else:
                    myagent.change_stat(
                        stat,
                        len(myagent.get_stat(stat).values)
                        - myagent.get_stat(stat).get_value(),
                    )
        myagent.clear_last_action()


def tick_decisionsys(myagent: agent.Agent, curtime: ztime.Time):
    print(curtime.hour())
    bio_needs(myagent, curtime)
    if myagent.is_idle():
        update_stats(myagent)
        decision = make_decisionsys(myagent, ACTIONS, STATS, curtime)
        if decision.get_msg() != "idle":
            myagent.set_action(decision)
