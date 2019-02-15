from src.flight_comp import CompState, Action
from src.stage import Stage
from src.state import VehicleState
from typing import Optional, List, Tuple


class Vehicle:
    """
    Stores data about vehicle and interprets actions from flight computer.
    """
    computer_state: CompState

    stage: Optional[Stage]
    remaining_engine_stages: List[Stage]
    parachute_stage: Optional[Stage]

    state: VehicleState

    def __init__(self,
                 computer_state: CompState,
                 stage: Optional[Stage],
                 remaining_engine_stages: List[Stage],
                 parachute_stage: Optional[Stage],
                 state: VehicleState):
        """
        :param computer_state: initial state of the computer.
        :param stage: current stage, e.g. engine being fired.
        :param remaining_engine_stages: list of stages which to be fired after current stage, in order which they should be fired.
        :param parachute_stage: stage to transition to to release parachute.
        :param state: current state of the vehicle.
        """
        self.computer_state = computer_state
        self.stage = stage
        self.remaining_engine_stages = remaining_engine_stages
        self.parachute_stage = parachute_stage
        self.state = state

    def step(self, dt: float) -> 'Vehicle':
        """
        :param dt: delta time, i.e. resolution.
        :return: next state of the vehicle.
        """
        new_total_time = self.state.time_s + dt
        next_state = self.state.step(new_total_time, self.stage)
        action, next_comp_state = self.computer_state.transition(self.state, next_state)
        next_stage, next_engine_stages = self._interpret(action)

        return Vehicle(next_comp_state, next_stage.step(dt), next_engine_stages, self.parachute_stage, next_state)

    def _interpret(self, action: Optional[Action]) -> Tuple[Stage, List[Stage]]:
        """
        :param action: from flight computer to perform.
        :return: next stage to perform, as well as any remaining engine stages.
        """
        if action is None:
            return self.stage, self.remaining_engine_stages

        elif action == Action.NEXT_STAGE:
            return self.remaining_engine_stages[0], self.remaining_engine_stages[1:]

        elif action == Action.PARACHUTE:
            if self.parachute_stage is None:
                raise RuntimeError('No parachute to eject')

            return self.parachute_stage, self.remaining_engine_stages

        raise RuntimeError('Unknown action')
