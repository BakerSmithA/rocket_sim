import pytest
from rocket_sim.state import VehicleState


@pytest.fixture
def zeroed_vehicle_states():
    return [VehicleState.zero(time/10) for time in range(0, 100)]

