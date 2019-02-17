from typing import List,Tuple
from .vehicle import Vehicle
from .state import VehicleState
from .calculations import apogee, maximum_acceleration, g_force
from .graphics import time_series_plot_group


class Simulation:

    def __init__(self, states: List[VehicleState]):
        self.states = states

    @property
    def events(self):
        return [(s.time_s, s.event) for s in self.states if s.event is not None]

    @property
    def impact_velocity(self) -> float:
        return self.states[-1].velocity_ms

    @property
    def maximum_acceleration(self) -> Tuple[float, float]:
        return maximum_acceleration(self.states)

    @property
    def maximum_velocity(self) -> Tuple[float, float]:
        max_vel_ms, max_vel_time_s = max([(s.velocity_ms, s.time_s) for s in self.states], key=lambda t: t[0])
        return max_vel_ms, max_vel_time_s

    @property
    def apogee(self) -> Tuple[float, float]:
        return apogee(self.states)

    @property
    def total_time(self) -> float:
        return self.states[-1].time_s

    @property
    def time_series(self) -> List[float]:
        return [s.time_s for s in self.states]

    @property
    def maximum_g_force(self):
        max_acceleration, max_acceleration_time = self.maximum_acceleration
        return g_force(max_acceleration), max_acceleration_time

    def display_plots(self, title) -> None:
        time_series_plot_group(title, [
            (self.time_series, [s.mass_kg for s in self.states], self.events, 'Time (s)', 'Mass (kg)'),
            (self.time_series, [s.accel_ms2 for s in self.states], self.events, 'Time (s)', 'Acceleration (m/s2)'),
            (self.time_series, [s.velocity_ms for s in self.states], self.events, 'Time (s)', 'Velocity (m/s)'),
            (self.time_series, [s.dist_m for s in self.states], self.events, 'Time (s)', 'Altitude (m)'),
            (self.time_series, [s.thrust_N for s in self.states], self.events, 'Time (s)', 'Thrust (N)'),
            (self.time_series, [s.air_resistance_N for s in self.states], self.events, 'Time(s)', 'Air Resistance (N)'),
        ])


def simulate(vehicle: Vehicle, dt: float) -> Simulation:
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

    apogee_m, apogee_time_s = apogee(states)

    for state in states:
        if state.dist_m == apogee_m and state.time_s == apogee_time_s:
            state.event = 'Apogee'

    return Simulation(states)


