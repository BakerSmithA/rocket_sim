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
        if now.velocity_ms < -7.0:
            return Action.PARACHUTE, comp_descent
        return None, comp_burn

    comp_burn.add_transition(deploy_parachute)

    burn_stage = Stage(area_m2=0.000979, drag_coefficient=0.75, empty_mass_kg=0.106, engine_case_mass_kg=0.0248,
                       propellant_mass_kg=0.0215, thrust_N=6.38, f_propellant_mass_kg=linear(-0.00342925),
                       f_thrust_N=const())

    # Mass as burn stage, as burn stage is not separated.
    parachute_stage = Stage(area_m2=0.02, drag_coefficient=0.75, empty_mass_kg=0.106, engine_case_mass_kg=0.0248,
                            propellant_mass_kg=0.0, thrust_N=0.0, f_propellant_mass_kg=const(),
                            f_thrust_N=const())

    return Vehicle(comp_burn, burn_stage, [], parachute_stage, VehicleState.zero())


def three_stage() -> Vehicle:
    """
    :return: description of two stage vehicle without a parachute.
    """
    comp_burn1 = Id('Burn Stage 1', [])
    comp_burn2 = Id('Burn Stage 2', [])
    comp_burn3 = Id('Burn Stage 3', [])

    # Computer deploys parachute after first stage runs out.
    def burn_stage(curr_state: CompState, comp_state: CompState) -> Callable:
        def burn_next_stage(prev: VehicleState, now: VehicleState, comp: CompState) -> Tuple[Optional[Action], CompState]:
            if now.dist_m > 10.0 and now.accel_ms2 <= 0.5:
                return Action.NEXT_STAGE, comp_state
            return None, curr_state

        return burn_next_stage

    comp_burn1.add_transition(burn_stage(comp_burn1, comp_burn2))
    comp_burn2.add_transition(burn_stage(comp_burn2, comp_burn3))

    stage3 = Stage(area_m2=0.000979, drag_coefficient=0.75, empty_mass_kg=0.106, engine_case_mass_kg=0.0248,
                   propellant_mass_kg=0.0215, thrust_N=6.38, f_propellant_mass_kg=linear(-0.00342925),
                   f_thrust_N=const())

    stage2 = Stage(area_m2=0.000979, drag_coefficient=0.75, empty_mass_kg=0.106+stage3.total_mass_kg(), engine_case_mass_kg=0.0248,
                   propellant_mass_kg=0.0215*2, thrust_N=6.38*2, f_propellant_mass_kg=linear(-0.00342925*2),
                   f_thrust_N=const())

    stage1 = Stage(area_m2=0.000979, drag_coefficient=0.75, empty_mass_kg=0.106+stage2.total_mass_kg(), engine_case_mass_kg=0.0248,
                   propellant_mass_kg=0.0215*3, thrust_N=6.38*3, f_propellant_mass_kg=linear(-0.00342925*3),
                   f_thrust_N=const())

    return Vehicle(comp_burn1, stage1, [stage2, stage3], None, VehicleState.zero())


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

    text_at_top = True
    for (event_time, event_name) in events:
        y = max(data) if text_at_top else min(data)
        plt.axvline(x=event_time, color='black', linewidth=0.5, linestyle='--')
        plt.text(x=event_time, y=y, s=event_name)
        text_at_top = not text_at_top

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


states = sim(single_stage(), 0.1)

apogee_m, apogee_time_s = max([(s.dist_m, s.time_s) for s in states], key=lambda t: t[0])
impact_velocity_ms = states[-1].velocity_ms
max_accel_ms2, max_accel_time_s = max([(s.accel_ms2, s.time_s) for s in states], key=lambda t: t[0])
total_time = states[-1].time_s

time = [s.time_s for s in states]
events = [(s.time_s, s.event) for s in states if s.event is not None]
events.append((apogee_time_s, 'Apogee'))

plot(time, [s.mass_kg for s in states], events, 'Time (s)', 'Mass (kg)')
plot(time, [s.accel_ms2 for s in states], events, 'Time (s)', 'Acceleration (m/s2)')
plot(time, [s.velocity_ms for s in states], events, 'Time (s)', 'Velocity (m/s)')
plot(time, [s.dist_m for s in states], events, 'Time (s)', 'Altitude (m)')

print('Apogee          (m):  ', apogee_m)
print('Time to apogee  (s):  ', apogee_time_s)
print('Time to land    (s):  ', total_time - apogee_time_s)
print('Time            (s):  ', total_time)
print('Impact Velocity (m/s):', impact_velocity_ms)
print('Max G-force:          ', max_accel_ms2 / 9.81)
print('Max G-force time (s): ', max_accel_time_s)
