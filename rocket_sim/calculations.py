from typing import List, Tuple
from .state import VehicleState


def apogee(states: List[VehicleState]) -> Tuple[float, float]:
    apogee_m, apogee_time_s = max([(s.dist_m, s.time_s) for s in states], key=lambda t: t[0])
    return apogee_m, apogee_time_s


def maximum_acceleration(states: List[VehicleState]) -> Tuple[float, float]:
    max_accel_ms2, max_accel_time_s = max([(s.accel_ms2, s.time_s) for s in states], key=lambda t: t[0])
    return max_accel_ms2, max_accel_time_s


def g_force(acceleration: float) -> float:
    return acceleration / 9.81
