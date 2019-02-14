from src.flight_comp import CompState, Action
from src.stage import Stage
from typing import List


class Vehicle:
    """
    Stores data about vehicle and interprets actions from flight computer.
    """
    computer_state: CompState
    engine_stages: List[Stage]
    parachute_stage: Stage

    def __init__(self, computer_state: CompState, engine_stages: List[Stage], parachute_stage: Stage):
        """
        :param computer_state: initial state of the computer.
        :param engine_stages: list of stages which can be fired, in order which they should be fired.
        :param parachute_stage: stage to transition to to release parachute.
        """
        self.computer_state = computer_state
        self.engine_stages = engine_stages
        self.parachute_stage = parachute_stage
