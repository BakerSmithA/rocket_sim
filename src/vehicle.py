from src.flight_comp import CompState, Action
from src.stage import Stage
from src.state import VehicleState
from typing import List


class Vehicle:
    """
    Stores data about vehicle and interprets actions from flight computer.
    """
    computer_state: CompState

    stage: Stage
    engine_stages: List[Stage]
    parachute_stage: Stage

    state: VehicleState
    total_time: float

    def __init__(self,
                 computer_state: CompState,
                 stage: Stage,
                 engine_stages: List[Stage],
                 parachute_stage: Stage,
                 state: VehicleState,
                 total_time: float):
        """
        :param computer_state: initial state of the computer.
        :param stage: current stage, e.g. engine being fired.
        :param engine_stages: list of stages which can be fired, in order which they should be fired.
        :param parachute_stage: stage to transition to to release parachute.
        :param state: current state of the vehicle.
        :param total_time: total time elapsed.
        """
        self.computer_state = computer_state
        self.stage = stage
        self.engine_stages = engine_stages
        self.parachute_stage = parachute_stage
        self.state = state
        self.total_time = total_time

    def step(self, dt: float) -> 'Vehicle':
        """
        :param dt: delta time, i.e. resolution.
        :return: next state of the vehicle.
        """
        new_total_time = self.total_time + dt

        next_state = self.state.step(new_total_time, self.stage)
        actions, next_comp_state = self.computer_state.transition(self.state, next_state)
        next_stage = self._interpret(actions).step(dt)

        return Vehicle(next_comp_state, next_stage, self.engine_stages, self.parachute_stage, next_state, new_total_time)

    def _interpret(self, actions: List[Action]) -> Stage:
        """
        :return: interpretation of next stage to 'segue' to.
        """
        pass
