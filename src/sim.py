from src.vehicle import Vehicle
from src.flight_comp import *
from src.stage import *
from src.state import VehicleState
import matplotlib.pyplot as plt


def single_stage() -> Vehicle:
    """
    :return: description of a single stage vehicle without a parachute.
    """
    comp_burn = Id('Burn', [])
    burn_stage = Stage(area_m2=0.000979, drag_coefficient=0.75, empty_mass_kg=0.106, engine_case_mass_kg=0.0248,
                       propellant_mass_kg=0.0215, thrust_N=6.38, f_propellant_mass_kg=linear(-0.00342925),
                       f_thrust_N=const())

    return Vehicle(comp_burn, burn_stage, [], None, VehicleState.zero())


def single_stage_parachute() -> Vehicle:
    """
    :return: description of a single stage vehicle with a parachute.
    """
    comp_burn = Id('Burn', [])
    comp_descent = Id('Descent', [])

    # Computer deploys parachute after starts falling.
    def deploy_parachute(prev: VehicleState, now: VehicleState, comp: CompState) -> Tuple[Optional[Action], CompState]:
        if now.velocity_ms < -5.0:
            return Action.PARACHUTE, comp_descent
        return None, comp_burn

    comp_burn.add_transition(deploy_parachute)

    burn_stage = Stage(area_m2=0.000979, drag_coefficient=0.75, empty_mass_kg=0.106, engine_case_mass_kg=0.0248,
                       propellant_mass_kg=0.0215, thrust_N=6.38, f_propellant_mass_kg=linear(-0.00342925),
                       f_thrust_N=const())

    parachute_stage = Stage(area_m2=0.08, drag_coefficient=0.75, empty_mass_kg=0.106, engine_case_mass_kg=0.0248,
                            propellant_mass_kg=0.0, thrust_N=0.0, f_propellant_mass_kg=const(),
                            f_thrust_N=const())

    return Vehicle(comp_burn, burn_stage, [], parachute_stage, VehicleState.zero())


def two_stage() -> Vehicle:
    """
    :return: description of two stage vehicle without a parachute.
    """
    comp_burn1 = Id('Burn Stage 1', [])
    comp_burn2 = Id('Burn Stage 2', [])

    # Computer deploys parachute after first stage runs out.
    def burn_stage2(prev: VehicleState, now: VehicleState, comp: CompState) -> Tuple[Optional[Action], CompState]:
        if now.dist_m > 10.0 and now.accel_ms2 <= 0.0:
            return Action.NEXT_STAGE, comp_burn2
        return None, comp_burn1

    comp_burn1.add_transition(burn_stage2)

    stage1 = Stage(area_m2=0.000979, drag_coefficient=0.75, empty_mass_kg=0.106*2, engine_case_mass_kg=0.0248,
                   propellant_mass_kg=0.0215, thrust_N=6.38, f_propellant_mass_kg=linear(-0.00342925),
                   f_thrust_N=const())

    stage2 = Stage(area_m2=0.000979, drag_coefficient=0.75, empty_mass_kg=0.106, engine_case_mass_kg=0.0248,
                   propellant_mass_kg=0.0215, thrust_N=6.38, f_propellant_mass_kg=linear(-0.00342925),
                   f_thrust_N=const())

    return Vehicle(comp_burn1, stage1, [stage2], None, VehicleState.zero())


def sim(v: Vehicle, dt: float) -> List[VehicleState]:
    """
    :param v: vehicle to simulate.
    :param dt: time step, i.e. resolution.
    :return: acceleration, velocity, and altitude of vehicle until it returns to ground.
    """
    states = []

    def touched_down() -> bool:
        if len(states) == 0:
            return False

        s = states[-1]
        return s.velocity_ms < 0 and s.dist_m <= 0

    while not touched_down():
        v = v.step(dt)
        states.append(v.state)

    return states


def plot(time: List[float], data: List[float], events: List[Tuple[float, str]], x_label: str, y_label: str):
    plt.plot(time, data)

    for (event_time, event_name) in events:
        plt.axvline(x=event_time, color='black', linewidth=0.5, linestyle='--')
        plt.text(x=event_time, y=max(data), s=event_name)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


states = sim(single_stage_parachute(), 0.1)

time = [s.time_s for s in states]
events = [(s.time_s, s.event) for s in states if s.event is not None]

plot(time, [s.mass_kg for s in states], events, 'Time (s)', 'Mass (kg)')
plot(time, [s.accel_ms2 for s in states], events, 'Time (s)', 'Acceleration (m/s2)')
plot(time, [s.velocity_ms for s in states], events, 'Time (s)', 'Velocity (m/s)')
plot(time, [s.dist_m for s in states], events, 'Time (s)', 'Altitude (m)')

apogee_m, apogee_time_s = max([(s.dist_m, s.time_s) for s in states], key=lambda t: t[0])
impact_velocity_ms = states[-1].velocity_ms
max_gforce = max([s.accel_ms2 for s in states]) / 9.81
total_time = states[-1].time_s

print('Apogee          (m):  ', apogee_m)
print('Time to apogee  (s):  ', apogee_time_s)
print('Time to land    (s):  ', total_time - apogee_time_s)
print('Time            (s):  ', total_time)
print('Impact Velocity (m/s):', impact_velocity_ms)
print('Max G-force:          ', max_gforce)
