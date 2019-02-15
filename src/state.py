from src.stage import Stage


class VehicleState:
    """
    State of rocket at given point in time. Used to record data to plot.
    """
    time_s: float
    mass_kg: float
    thrust_N: float
    air_resistance_N: float
    weight_N: float
    net_force: float
    accel_ms2: float
    velocity_ms: float
    dist_m: float

    def __init__(self,  time_s: float, mass_kg: float, thrust_N: float, air_resistance_N: float, weight_N: float, net_force_N, accel_ms: float, velocity_ms: float, dist_m: float):
        self.time_s = time_s
        self.mass_kg = mass_kg
        self.thrust_N = thrust_N
        self.net_force_N = net_force_N
        self.air_resistance_N = air_resistance_N
        self.weight_N = weight_N
        self.accel_ms2 = accel_ms
        self.velocity_ms = velocity_ms
        self.dist_m = dist_m

    def step(self, dt: float, time_s: float, stage: Stage) -> 'VehicleState':
        dry_mass_kg = stage.empty_mass_kg + stage.engine_case_mass_kg
        wet_mass_kg = dry_mass_kg + stage.propellant_mass_kg

        # 0.5*rho*Cd*A*SIGN(V)*V^2
        air_resistance_N = 0.5 * 1.2 * stage.drag_coefficient * stage.area_m2 * self.velocity_ms * abs(self.velocity_ms)
        weight_N = wet_mass_kg * 9.81
        thrust_N = stage.thrust_N
        net_force_N = thrust_N - weight_N - air_resistance_N

        accel_ms2 = net_force_N / wet_mass_kg
        velocity_ms = self.velocity_ms + accel_ms2 * dt
        dist_m = self.dist_m + self.velocity_ms * dt + 0.5 * self.accel_ms2 * dt**2

        return VehicleState(time_s, wet_mass_kg, thrust_N, air_resistance_N, weight_N, net_force_N, accel_ms2, velocity_ms, dist_m)

    @staticmethod
    def zero() -> 'VehicleState':
        return VehicleState(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
