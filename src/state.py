from src.stage import Stage


class VehicleState:
    """
    State of rocket at given point in time.
    """
    time_s: float
    mass_kg: float
    thrust_N: float
    drag_N: float

    def __init__(self, time_s: float, mass_kg: float, drag_N: float, thrust_N: float):
        self.time_s = time_s
        self.mass_kg = mass_kg
        self.drag_N = drag_N
        self.thrust_N = thrust_N

    @classmethod
    def from_stage(cls, time_s: float, stage: Stage) -> 'VehicleState':
        mass_kg = stage.empty_mass_kg + stage.engine_case_mass_kg + stage.propellant_mass_kg
        drag_N = 0.0
        total_N = stage.thrust_N - drag_N

        return VehicleState(time_s, mass_kg, stage.thrust_N, total_N)
