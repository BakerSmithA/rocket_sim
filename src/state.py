from src.stage import Stage


class VehicleState:
    """
    State of rocket at given point in time. Used to record data to plot.
    """
    time_s: float
    mass_kg: float
    thrust_N: float
    drag_N: float
    accel_ms2: float
    velocity_ms: float
    dist_m: float

    def __init__(self, time_s: float, mass_kg: float, drag_N: float, thrust_N: float, accel_ms: float, velocity_ms: float, dist_m: float):
        self.time_s = time_s
        self.mass_kg = mass_kg
        self.drag_N = drag_N
        self.thrust_N = thrust_N
        self.accel_ms2 = accel_ms
        self.velocity_ms = velocity_ms
        self.dist_m = dist_m

    def step(self, time_s: float, stage: Stage) -> 'VehicleState':
        mass_kg = stage.empty_mass_kg + stage.engine_case_mass_kg + stage.propellant_mass_kg
        drag_N = -9.81 * mass_kg
        total_N = stage.thrust_N + drag_N
        accel_ms2 = total_N / mass_kg
        velocity_ms = self.velocity_ms + accel_ms2
        dist_m = self.dist_m + self.velocity_ms

        return VehicleState(time_s, mass_kg, stage.thrust_N, total_N, accel_ms2, velocity_ms, dist_m)

    @staticmethod
    def zero() -> 'VehicleState':
        return VehicleState(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
