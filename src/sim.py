from src.vehicle import Vehicle
from src.flight_comp import *
from src.stage import *
from src.state import VehicleState
import matplotlib.pyplot as plt


def single_stage() -> Vehicle:
    """
    :return: description of a single stage vehicle without a parachute.
    """
    comp_burn = Id('Burn', [])
    burn_stage = Stage(area_m2=0.5, empty_mass_kg=1.0, engine_case_mass_kg=0.015, propellant_mass_kg=0.0015,
                       thrust_N=15.0, f_propellant_mass_kg=linear(-0.00075), f_thrust_N=const())
    state = VehicleState.zero()

    return Vehicle(comp_burn, burn_stage, [], None, state)


def sim(v: Vehicle) -> List[VehicleState]:
    """
    :param v: vehicle to simulate.
    :return: acceleration, velocity, and altitude of vehicle until it returns to ground.
    """
    dt = 0.1
    end_time_s = 5.0
    curr_time = 0.0

    states = []

    while curr_time < end_time_s:
        v = v.step(dt)
        states.append(v.state)

        curr_time += dt

    return states


def plot(data: List[float], x_label: str, y_label: str):
    plt.plot(data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


states = sim(single_stage())

plot([s.dist_m for s in states], 'Time (s)', 'Altitude (m)')
plot([s.velocity_ms for s in states], 'Time (s)', 'Velocity (m/s)')
plot([s.accel_ms2 for s in states], 'Time (s)', 'Acceleration (m/s2)')
