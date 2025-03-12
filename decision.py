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
    chosen_Action = action.Action(best_Action, curtime, actions.get(_action)[2])

    return chosen_Action


def tick_decisionsys(myagent: agent.Agent, curtime: ztime.Time):
    if myagent.is_idle():
        decision = make_decisionsys(myagent, ACTIONS, STATS, curtime)
        if decision.get_msg() != "vibing":
            myagent.set_action(decision)
