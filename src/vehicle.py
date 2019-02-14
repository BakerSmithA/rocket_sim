from src.flight_comp import CompState, Action
from src.stage import Stage
from src.state import VehicleState
from typing import Optional, List, Tuple


class Vehicle:
    """
    Stores data about vehicle and interprets actions from flight computer.
    """
    computer_state: CompState

    stage: Stage
    curr_engine_stage: int
    engine_stages: List[Stage]
    parachute_stage: Stage

    state: VehicleState

    def __init__(self,
                 computer_state: CompState,
                 stage: Stage,
                 curr_engine_stage: int,
                 engine_stages: List[Stage],
                 parachute_stage: Stage,
                 state: VehicleState):
        """
        :param computer_state: initial state of the computer.
        :param stage: current stage, e.g. engine being fired.
        :param engine_stages: list of stages which can be fired, in order which they should be fired.
        :param parachute_stage: stage to transition to to release parachute.
        :param state: current state of the vehicle.
        """
        self.computer_state = computer_state
        self.stage = stage
        self.curr_engine_stage = curr_engine_stage
        self.engine_stages = engine_stages
        self.parachute_stage = parachute_stage
        self.state = state

    def step(self, dt: float) -> 'Vehicle':
        """
        :param dt: delta time, i.e. resolution.
        :return: next state of the vehicle.
        """
        new_total_time = self.state.time_s + dt

        actions, next_comp_state = self.computer_state.transition(self.state, self.state)
        next_engine_stage, next_stage = self._interpret(actions)
        next_stage = next_stage.step(dt)

        next_state = self.state.step(new_total_time, next_stage)

        return Vehicle(next_comp_state, next_stage, next_engine_stage, self.engine_stages,
                       self.parachute_stage, next_state)

    def _interpret(self, action: Optional[Action]) -> Tuple[int, Stage]:
        """
        :return: interpretation of next stage to 'segue' to.
        """
        if action is None:
            return self.curr_engine_stage, self.stage
        elif action == Action.NEXT_STAGE:
            return self.curr_engine_stage+1, self.engine_stages[self.curr_engine_stage+1]
        elif action == Action.PARACHUTE:
            return self.curr_engine_stage, self.parachute_stage

        raise RuntimeError('Bad action')

