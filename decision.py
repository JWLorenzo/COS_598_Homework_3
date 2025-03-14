import enum
import ztime
import action
from defs import STATS, ACTIONS, BIO_STATS
import agent
import math

## Make sure to remove this
import random


def get_discontentment(value: float) -> float:
    return value * value


def discontentment(
    myagent: agent.Agent, action: list[list, dict, ztime.Time], goals: list
) -> float:
    discontentment_Value = 0

    for goal in goals:
        new_Value = abs(
            (myagent.get_stat(goal).get_value() + action[1].get(goal, 0))
            / (len(myagent.get_stat(goal).values) - 1)
        )
        if (
            myagent.get_stat(goal).get_value() == 0
            and max(0, myagent.get_stat(goal).get_value() + action[1].get(goal, 0)) == 0
        ):
            if action[1].get(goal, 0) != 0:
                new_Value = 1
        discontentment_Value += get_discontentment(new_Value)
    return discontentment_Value


def check_time(
    actions: dict, _action: str, curtime: ztime.Time, this_Value: float
) -> float:
    if actions.get(_action)[4][0] or actions.get(_action)[4][1]:
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
    return this_Value


def make_decisionsys(
    myagent: agent.Agent, actions: dict, goals: dict, curtime: ztime.Time
) -> action.Action:
    best_Action = "idle"
    best_Value = math.inf

    for _action in list(actions.keys())[1:]:

        this_Value = discontentment(
            myagent, actions.get(_action), list(goals.keys())[1:]
        )
        this_Value = check_time(actions, _action, curtime, this_Value)
        if (myagent.get_stat("location").get_value() in actions.get(_action)[0]) or (
            "anywhere" in actions.get(_action)[0]
        ):
            if this_Value < best_Value:
                best_Value = this_Value
                best_Action = _action
        else:
            this_Value += discontentment(
                myagent,
                actions.get("drive"),
                ["debt"],
            )
            this_Value = check_time(actions, "drive", curtime, this_Value)
            if this_Value < best_Value:
                best_Value = this_Value
                best_Action = "drive"
                myagent.location = actions.get(_action)[0][0]
        print("chosen action", _action)
        print("discontentment", this_Value)
    if "job" in best_Action:
        time_modifier = ztime.Time(actions.get(best_Action)[2] - curtime.minit())
    else:
        time_modifier = ztime.Time(actions.get(best_Action)[2])
    print("final action", best_Action)
    chosen_Action = action.Action(best_Action, curtime, curtime.__add__(time_modifier))
    print("-" * 20)
    return chosen_Action


def bio_needs(myagent: agent.Agent, curtime: ztime.Time):
    if (
        (curtime.hour() % 2 == 0)
        and (curtime.minit() == 0)
        and (myagent.last_bio != curtime.hour())
    ):
        for stat in BIO_STATS:
            max_value = len(myagent.get_stat(stat).values) - 1
            rand_stat_increase = random.randint(0, 2)
            calculated_total = myagent.get_stat(stat).get_value() + rand_stat_increase

            if myagent.action != None:
                if stat not in ACTIONS.get(myagent.action.get_msg())[3]:
                    if calculated_total >= 0 and calculated_total < max_value:
                        myagent.change_stat(stat, rand_stat_increase)
                    else:
                        myagent.change_stat(
                            stat,
                            (len(myagent.get_stat(stat).values) - 1)
                            - myagent.get_stat(stat).get_value(),
                        )
            else:
                if calculated_total >= 0 and calculated_total < max_value:
                    myagent.change_stat(stat, rand_stat_increase)
                else:
                    myagent.change_stat(
                        stat,
                        (len(myagent.get_stat(stat).values) - 1)
                        - myagent.get_stat(stat).get_value(),
                    )
        myagent.last_bio = curtime.hour()


def update_stats(myagent: agent.Agent) -> None:
    if myagent.last_action != None and myagent.last_action.get_msg() != "idle":
        if myagent.last_action.get_msg() == "drive":
            myagent.change_stat(
                "location",
                (
                    STATS.get("location").index(myagent.location)
                    - STATS.get("location").index(
                        myagent.get_stat("location").get_value()
                    )
                ),
            )
        for stat in list(STATS.keys())[1:]:
            calculated_total = myagent.get_stat(stat).get_value() + ACTIONS.get(
                myagent.last_action.get_msg()
            )[1].get(stat, 0)

            if calculated_total >= 0:
                if calculated_total < len(myagent.get_stat(stat).values) - 1:
                    diff = ACTIONS.get(myagent.last_action.get_msg())[1].get(stat, 0)
                    myagent.change_stat(stat, diff)
                elif calculated_total >= len(myagent.get_stat(stat).values) - 1:
                    diff = (len(myagent.get_stat(stat).values) - 1) - myagent.get_stat(
                        stat
                    ).get_value()
                    myagent.change_stat(stat, diff)
            else:
                diff = -myagent.get_stat(stat).get_value()
                myagent.change_stat(stat, diff)
        myagent.clear_last_action()


def tick_decisionsys(myagent: agent.Agent, curtime: ztime.Time):
    # print(curtime.hour())
    bio_needs(myagent, curtime)
    if myagent.is_idle():
        update_stats(myagent)
        decision = make_decisionsys(myagent, ACTIONS, STATS, curtime)
        if decision.get_msg() != "idle":
            myagent.set_action(decision)
