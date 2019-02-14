from src.state import VehicleState
from typing import Tuple, Callable, TypeVar, List, Optional
from enum import Enum


class Action(Enum):
    """
    Actions the flight computer can instruct the vehicle to perform.
    """
    STAGE_SEP = 0
    FIRE_MOTOR = 1
    PARACHUTE = 2


T = TypeVar('T')


"""
Mapping from previous and current vehicle states, and the current computer state, to the actions to take and the 
next computer state.
"""
transition = Callable[[VehicleState, VehicleState, T], Optional[Tuple[List[Action], 'CompState']]]


class CompState:
    """
    Stores state of flight computer and makes transitions to new computer states.
    """
    ts: List[transition]

    def __init__(self, ts: List[transition]):
        self.ts = ts

    def add_transition(self, t: transition):
        self.ts.append(t)

    def transition(self, prev: VehicleState, now: VehicleState) -> Tuple[[List[Action]], 'CompState']:
        """
        :param prev: previous state of vehicle.
        :param now: current state of vehicle.
        :return: check whether a transition can be performed, and if so performs the transition.
            Otherwise, updates the current computer state and returns that.
        """
        pass

    def check(self, prev: VehicleState, now: VehicleState) -> Optional[Tuple[[List[Action]], 'CompState']]:
        """
        Helper method for subclasses.
        :param prev: previous state of vehicle.
        :param now: current state of vehicle.
        :return: check whether a transition can be performed, and if so performs the transition.
            Otherwise, returns None.
        """
        for t in self.ts:
            r = t(prev, now, self)
            if r is not None:
                return r

        return None


class Timer(CompState):
    """
    Counts down time to zero.
    """
    time_rem_s: float

    def __init__(self, ts: List[transition], time_rem_s: float):
        """
        :param ts: transitions from state.
        :param time_rem_s: time to count down from.
        """
        super(Timer, self).__init__(ts)
        self.time_rem_s = time_rem_s

    def transition(self, prev: VehicleState, now: VehicleState) -> Tuple[[List[Action]], CompState]:
        r = self.check(prev, now)
        if r is not None:
            return r

        dt = now.time_s - prev.time_s
        return [], Timer(self.ts, self.time_rem_s - dt)


class Id(CompState):
    """
    Flight computer state that does not change over time.
    """
    def transition(self, prev: VehicleState, now: VehicleState) -> Tuple[[List[Action]], CompState]:
        r = self.check(prev, now)
        if r is not None:
            return r

        return [], Id(self.ts)
