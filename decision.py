import enum
import ztime
import action
from defs import STATS, ACTIONS
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
        new_Value = max(0, myagent.get_stat(goal).get_value() + action[1].get(goal, 0))

        discontentment_Value += getDiscontentment(new_Value)

    return discontentment_Value


def make_decisionsys(
    myagent: agent.Agent, actions: dict, goals: dict, curtime: ztime.Time
) -> action.Action:
    best_Action = ""
    best_Value = math.inf

    for _action in list(actions.keys()):
        this_Value = discontentment(myagent, actions.get(_action), goals)
        if this_Value < best_Value:
            best_Value = this_Value
            best_Action = _action
    time_modifier = ztime.Time(actions.get(best_Action)[2])
    chosen_Action = action.Action(best_Action, curtime, curtime.__add__(time_modifier))

    return chosen_Action


def tick_decisionsys(myagent: agent.Agent, curtime: ztime.Time):
    # print(myagent.get_action())

    if myagent.is_idle():
        if myagent.last_action != None and myagent.last_action.get_msg() != "vibing":
            for stat in list(STATS.keys())[1:]:
                # print("checking")
                # print(myagent.get_stat(stat).get_value())
                # print(myagent.last_action.get_msg())
                # print(ACTIONS.get(myagent.last_action))
                if (
                    myagent.get_stat(stat).get_value()
                    + ACTIONS.get(myagent.last_action.get_msg())[1].get(stat, 0)
                    >= 0
                ):
                    myagent.change_stat(
                        stat, ACTIONS.get(myagent.last_action.get_msg())[1].get(stat, 0)
                    )
                else:
                    myagent.change_stat(stat, -myagent.get_stat(stat).get_value())
            myagent.clear_last_action()

        decision = make_decisionsys(myagent, ACTIONS, STATS, curtime)
        if decision.get_msg() != "vibing":
            myagent.set_action(decision)
            # print(myagent.get_action().get_msg())
