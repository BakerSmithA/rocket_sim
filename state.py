
class State:
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

