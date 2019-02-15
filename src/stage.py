from typing import Type, Callable, TypeVar

T = TypeVar('T')
total_time_s = float
delta_time_s = float


def param(X: Type) -> Type:
    """
    Return type of time based function, i.e. (Time, X) -> X
    :param X: type returned by time dependent function.
    :return: type of a function dependent on elapsed time and previous value.
    """
    return Callable[[delta_time_s, X], X]


def const() -> param(T):
    """
    Parameter of stage which does not change over time from initial value.
    :return: function which returns previous value.
    """
    return lambda _, prev_x: prev_x


def linear(dx_per_sec: T) -> T:
    """
    Increase/decrease amount linearly.
    :param dx_per_sec: amount to modify by per second.
    :return: function which decreases x by dx_per_sec per second.
    """
    def f(dt: delta_time_s, prev_x: T) -> T:
        dx = dx_per_sec * dt
        return prev_x + dx

    return f


class Stage:
    """
    Defines how rocket changes over time.
    """
    area_m2: float
    drag_coefficient: float
    empty_mass_kg: float
    engine_case_mass_kg: float

    propellant_mass_kg: float
    impulse_Ns: float
    thrust_N: float

    f_propellant_mass_kg: param(float)
    f_thrust_N: param(float)

    def __init__(self,
                 area_m2: float,
                 drag_coefficient: float,
                 empty_mass_kg: float,
                 engine_case_mass_kg: float,
                 propellant_mass_kg: float,
                 thrust_N: float,
                 f_propellant_mass_kg: param(float),
                 f_thrust_N: param(float)):

        self.area_m2 = area_m2
        self.drag_coefficient = drag_coefficient
        self.empty_mass_kg = empty_mass_kg
        self.engine_case_mass_kg = engine_case_mass_kg

        self.propellant_mass_kg = propellant_mass_kg
        self.thrust_N = thrust_N

        self.f_propellant_mass_kg = f_propellant_mass_kg
        self.f_thrust_N = f_thrust_N

    def step(self, dt: delta_time_s) -> 'Stage':
        """
        :param dt: delta time since last step.
        :return: new state of the stage, e.g. with decreased mass.
        """
        if self.propellant_mass_kg > 0.0:
            new_prop_mass = max(self.f_propellant_mass_kg(dt, self.propellant_mass_kg), 0.0)
            new_thrust_N = self.f_thrust_N(dt, self.thrust_N)
        else:
            new_prop_mass = 0.0
            new_thrust_N = 0.0

        return Stage(self.area_m2, self.drag_coefficient, self.empty_mass_kg, self.engine_case_mass_kg, new_prop_mass,
                     new_thrust_N, self.f_propellant_mass_kg, self.f_thrust_N)
