from typing import Tuple, Optional, Callable
from rocket_sim.vehicle import Vehicle, VehicleState
from rocket_sim.flight_comp import Action, CompState, Id
from rocket_sim.stage import Stage, linear, const


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
    def deploy_parachute(_prev: VehicleState, now: VehicleState, _comp: CompState) -> Tuple[Optional[Action], CompState]:
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

    stage3 = Stage(area_m2=0.000979,
                   drag_coefficient=0.75,
                   empty_mass_kg=0.106,
                   engine_case_mass_kg=0.0248,
                   propellant_mass_kg=0.0215,
                   thrust_N=6.38,
                   f_propellant_mass_kg=linear(-0.00342925),
                   f_thrust_N=const(),
                   )

    stage2 = Stage(area_m2=0.000979,
                   drag_coefficient=0.75,
                   empty_mass_kg=0.106+stage3.total_mass_kg(),
                   engine_case_mass_kg=0.0248,
                   propellant_mass_kg=0.0215*2,
                   thrust_N=6.38*2,
                   f_propellant_mass_kg=linear(-0.00342925*2),
                   f_thrust_N=const(),
                   )

    stage1 = Stage(area_m2=0.000979,
                   drag_coefficient=0.75,
                   empty_mass_kg=0.106+stage2.total_mass_kg(),
                   engine_case_mass_kg=0.0248,
                   propellant_mass_kg=0.0215*3,
                   thrust_N=6.38*3,
                   f_propellant_mass_kg=linear(-0.00342925*3),
                   f_thrust_N=const(),
                   )

    return Vehicle(comp_burn1, stage1, [stage2, stage3], None, VehicleState.zero())
