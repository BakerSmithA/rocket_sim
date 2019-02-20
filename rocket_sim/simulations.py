from typing import List, Tuple, Callable
from .vehicle import Vehicle
from .state import VehicleState
from .graphics import time_series_plot_group


class Simulation:

    def __init__(self, states: List[VehicleState]):
        self.states = states

    def _max_val(self, get_val: Callable[[VehicleState], float]) -> Tuple[float, float]:
        """
        :param get_val: return value to find maximum of.
        :return: maximum value and time occurred.
        """
        vs = [(get_val(s), s.time_s) for s in self.states]
        return max(vs, key=lambda v: v[0])

    @property
    def events(self):
        es = [(s.time_s, s.event) for s in self.states if s.event is not None]

        _, t = self.apogee
        es.append((t, 'Apogee'))

        return es

    @property
    def maximum_g_force(self) -> Tuple[float, float]:
        g = 9.81
        (a, t) = self._max_val(lambda s: s.accel_ms2)
        return a/g, t

    @property
    def impact_velocity(self) -> float:
        return self.states[-1].velocity_ms

    @property
    def maximum_acceleration(self) -> Tuple[float, float]:
        return self._max_val(lambda s: s.accel_ms2)

    @property
    def maximum_velocity(self) -> Tuple[float, float]:
        return self._max_val(lambda s: s.velocity_ms)

    @property
    def apogee(self) -> Tuple[float, float]:
        return self._max_val(lambda s: s.dist_m)

    @property
    def total_time(self) -> float:
        return self.states[-1].time_s

    @property
    def time_series(self) -> List[float]:
        return [s.time_s for s in self.states]

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

    t = 0.0
    while not touched_down() or t < 5.0:
        vehicle = vehicle.step(dt)
        states.append(vehicle.state)
        t += dt

    return Simulation(states)
