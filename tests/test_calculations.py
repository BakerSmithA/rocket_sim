import pytest
from rocket_sim.simulations import Simulation


def test_apogee(zeroed_vehicle_states):
    zeroed_vehicle_states[-1].dist_m = 100
    sim = Simulation(zeroed_vehicle_states)
    height, time = sim.apogee

    assert height == 100
    assert time == zeroed_vehicle_states[-1].time_s


def test_maximum_acceleration(zeroed_vehicle_states):
    zeroed_vehicle_states[-1].accel_ms2 = 100
    sim = Simulation(zeroed_vehicle_states)
    max_acceleration, time = sim.maximum_acceleration

    assert max_acceleration == 100
    assert time == zeroed_vehicle_states[-1].time_s

