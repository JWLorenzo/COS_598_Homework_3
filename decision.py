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

    for _action in list(actions.keys()):
        this_Value = discontentment(myagent, actions.get(_action), goals)
        if this_Value < best_Value:
            best_Value = this_Value
            best_Action = _action
    time_modifier = ztime.Time(actions.get(best_Action)[2])
    chosen_Action = action.Action(best_Action, curtime, curtime.__add__(time_modifier))

    return chosen_Action


def bio_needs(myagent: agent.Agent, curtime: ztime.Time):
    # Stats that increase on a regular basis:
    # hunger, thirst, sleep, recreation, motivation, social, hygeine
    # print("check time")
    print("cur", curtime.hour())
    print("bio", myagent.last_bio.hour())
    if (curtime.hour() % 2 == 0) and (
        curtime.minit() == 0 and myagent.last_bio.hour() != curtime.hour()
    ):
        # print("bingo")
        for stat in BIO_STATS:
            if myagent.action != None:
                if stat not in ACTIONS.get(myagent.action.get_msg())[3]:
                    myagent.change_stat(stat, 1)
                    print("increasing1", stat)

            else:
                print("increasing2", stat)
                myagent.change_stat(stat, 1)
        myagent.last_bio = curtime


def update_stats(myagent: agent.Agent) -> None:
    if myagent.last_action != None and myagent.last_action.get_msg() != "idle":
        for stat in list(STATS.keys())[1:]:
            # print("checking")
            # print(myagent.get_stat(stat).get_value())
            # print(myagent.last_action.get_msg())
            # print(ACTIONS.get(myagent.last_action))
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
    bio_needs(myagent, curtime)
    if myagent.is_idle():
        update_stats(myagent)
        decision = make_decisionsys(myagent, ACTIONS, STATS, curtime)
        if decision.get_msg() != "idle":
            myagent.set_action(decision)
            # print(myagent.get_action().get_msg())
