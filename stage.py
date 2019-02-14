from typing import Type, Callable, TypeVar

T = TypeVar('T')
time_s = float


def param(X: Type) -> Type:
    """
    Return type of time based function, i.e. Time -> X
    :param X: type returned by time dependent function.
    :return: type of a time dependent function.
    """
    return Callable[[time_s], X]


def const(x: T) -> Callable[[time_s], T]:
    """
    Parameter of stage which does not change over time.
    :param x: returned by returned function.
    :return: function which returns constant x.
    """
    return lambda _: x


class Stage:
    """
    Defines how rocket changes over time.
    """
    empty_mass_kg: param(float)
    engine_case_mass_kg: param(float)
    propellant_mass_kg: param(float)
    impulse_Ns: param(float)
    thrust_N: param(float)
    area_m2: param(float)

    def __init__(self,
                 empty_mass_kg: param(float),
                 engine_case_mass_kg: param(float),
                 propellant_mass_kg: param(float),
                 impulse_Ns: param(float),
                 thrust_N: param(float),
                 area_m2: param(float)):

        self.empty_mass_kg = empty_mass_kg
        self.engine_case_mass_kg = engine_case_mass_kg
        self.propellant_mass_kg = propellant_mass_kg
        self.impulse_Ns = impulse_Ns
        self.thrust_N = thrust_N
        self.area_m2 = area_m2
