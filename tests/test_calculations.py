import pytest
from rocket_sim.calculations import g_force, apogee, maximum_acceleration


def test_apogee(zeroed_vehicle_states):
    zeroed_vehicle_states[-1].dist_m = 100
    height, time = apogee(zeroed_vehicle_states)

    assert height == 100
    assert time == zeroed_vehicle_states[-1].time_s


def test_maximum_acceleration(zeroed_vehicle_states):
    zeroed_vehicle_states[-1].accel_ms2 = 100
    max_acceleration, time = maximum_acceleration(zeroed_vehicle_states)

    assert max_acceleration == 100
    assert time == zeroed_vehicle_states[-1].time_s


@pytest.mark.parametrize("acceleration, gs", [
    (9.81, 1),
    (0, 0),
    (19.62, 2),
])
def test_g_force(acceleration, gs):
    assert g_force(acceleration) == gs
