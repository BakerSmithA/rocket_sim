from typing import List
from .vehicle import Vehicle
from .state import VehicleState


def simulate(vehicle: Vehicle, dt: float) -> List[VehicleState]:
    """
    :param vehicle: vehicle to simulate.
    :param dt: time step, i.e. resolution.
    :return: acceleration, velocity, and altitude of vehicle until it returns to ground.
    """
    states: List[VehicleState] = []

    def touched_down() -> bool:
        if len(states) == 0:
            return False

        s = states[-1]
        return s.velocity_ms < 0 and s.dist_m <= 0

    while not touched_down():
        vehicle = vehicle.step(dt)
        states.append(vehicle.state)

    return states


