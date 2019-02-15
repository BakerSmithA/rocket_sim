from src.stage import Stage


def sign(x: float) -> float:
    return 1.0 if x >= 0 else -1.0


class VehicleState:
    """
    State of rocket at given point in time. Used to record data to plot.
    """
    time_s: float
    mass_kg: float
    accel_ms2: float
    velocity_ms: float
    dist_m: float

    def __init__(self, time_s: float, mass_kg: float, accel_ms: float, velocity_ms: float, dist_m: float):
        self.time_s = time_s
        self.mass_kg = mass_kg
        self.accel_ms2 = accel_ms
        self.velocity_ms = velocity_ms
        self.dist_m = dist_m

    def step(self, time_s: float, stage: Stage) -> 'VehicleState':
        mass_kg = stage.empty_mass_kg + stage.engine_case_mass_kg + stage.propellant_mass_kg

        weight_N = 9.81 * mass_kg
        # 0.5 * rho * Cd * A * SIGN(V) * V ^ 2
        air_resistance_N = 0.5 * 1.2 * stage.drag_coefficient * stage.area_m2 * sign(self.velocity_ms) * self.velocity_ms * self.velocity_ms
        drag_N = weight_N + air_resistance_N
        total_N = stage.thrust_N - drag_N

        accel_ms2 = total_N / mass_kg
        velocity_ms = self.velocity_ms + accel_ms2
        dist_m = self.dist_m + self.velocity_ms

        return VehicleState(time_s, mass_kg, accel_ms2, velocity_ms, dist_m)

    @staticmethod
    def zero() -> 'VehicleState':
        return VehicleState(0.0, 0.0, 0.0, 0.0, 0.0)
