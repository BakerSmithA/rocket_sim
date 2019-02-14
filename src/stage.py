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


def const(x: T) -> param(T):
    """
    Parameter of stage which does not change over time.
    :param x: returned by returned function.
    :return: function which returns constant x.
    """
    return lambda dt, prev_x: x


def choice(threshold_s: total_time_s, pre: T, post: T) -> param(T):
    """
    :param threshold_s: time to switch value returned.
    :param pre: value to return while t < threshold
    :param post: value to return while time >= threshold_s
    :return: pre if time is below the threshold, and return post otherwise.
    """
    total_time = 0.0

    def f(dt: delta_time_s) -> T:
        nonlocal total_time
        total_time += dt
        if total_time <= threshold_s:
            return pre
        return post

    return f


class Stage:
    """
    Defines how rocket changes over time.
    """
    area_m2: float
    empty_mass_kg: float
    engine_case_mass_kg: float

    propellant_mass_kg: float
    impulse_Ns: float
    thrust_N: float

    step_propellant_mass_kg: param(float)
    step_impulse_Ns: param(float)
    step_thrust_N: param(float)

    def __init__(self,
                 area_m2: float,
                 impulse_Ns: float,
                 empty_mass_kg: float,
                 engine_case_mass_kg: float,
                 propellant_mass_kg: float,
                 thrust_N: float,
                 step_propellant_mass_kg: param(float),
                 step_thrust_N: param(float)):

        self.area_m2 = area_m2
        self.impulse_Ns = impulse_Ns
        self.empty_mass_kg = empty_mass_kg
        self.engine_case_mass_kg = engine_case_mass_kg

        self.propellant_mass_kg = propellant_mass_kg
        self.thrust_N = thrust_N

        self.step_propellant_mass_kg = step_propellant_mass_kg
        self.step_thrust_N = step_thrust_N

    def step(self, dt: delta_time_s) -> 'Stage':
        """
        :param dt: delta time since last step.
        :return: new state of the stage, e.g. with decreased mass.
        """
        new_prop_mass = self.step_propellant_mass_kg(dt, self.propellant_mass_kg)
        new_thrust_N = self.step_thrust_N(dt, self.thrust_N)

        return Stage(self.area_m2, self.impulse_Ns, self.empty_mass_kg, self.engine_case_mass_kg, new_prop_mass,
                     new_thrust_N, self.step_propellant_mass_kg, self.step_thrust_N)
