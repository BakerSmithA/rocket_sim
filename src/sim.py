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


def sim(v: Vehicle, dt: float) -> List[VehicleState]:
    """
    :param v: vehicle to simulate.
    :param dt: time step, i.e. resolution.
    :return: acceleration, velocity, and altitude of vehicle until it returns to ground.
    """
    dt = 0.1
    states = []

    def touched_down() -> bool:
        if len(states) == 0:
            return False

        s = states[-1]
        return s.velocity_ms < 0 and s.dist_m <= 0

    while not touched_down():
        v = v.step(dt)
        states.append(v.state)

    return states


def plot(data: List[float], x_label: str, y_label: str):
    plt.plot(data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


states = sim(single_stage(), 0.1)

plot([s.dist_m for s in states], 'Time (s)', 'Altitude (m)')
plot([s.velocity_ms for s in states], 'Time (s)', 'Velocity (m/s)')
plot([s.accel_ms2 for s in states], 'Time (s)', 'Acceleration (m/s2)')
