from src.stage import Stage


class VehicleState:
    """
    State of rocket at given point in time. Used to record data to plot.
    """
    time_s: float
    mass_kg: float
    accel_ms2: float
    velocity_ms: float
    dist_m: float

    def __init__(self,  time_s: float, mass_kg: float, accel_ms: float, velocity_ms: float, dist_m: float):
        self.time_s = time_s
        self.mass_kg = mass_kg
        self.accel_ms2 = accel_ms
        self.velocity_ms = velocity_ms
        self.dist_m = dist_m

    def step(self, dt: float, time_s: float, stage: Stage) -> 'VehicleState':
        dry_mass_kg = stage.empty_mass_kg + stage.engine_case_mass_kg
        wet_mass_kg = dry_mass_kg + stage.propellant_mass_kg

        weight_N = wet_mass_kg * 9.81
        thrust_N = stage.thrust_N
        net_force_N = thrust_N - weight_N

        accel_ms2 = net_force_N / wet_mass_kg
        velocity_ms = self.velocity_ms + accel_ms2
        dist_m = self.dist_m + velocity_ms

        return VehicleState(time_s, wet_mass_kg, accel_ms2, velocity_ms, dist_m)

    @staticmethod
    def zero() -> 'VehicleState':
        return VehicleState(0.0, 0.0, 0.0, 0.0, 0.0)
