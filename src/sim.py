from src.vehicle import Vehicle
from src.flight_comp import *
from src.stage import *
from src.state import VehicleState
import matplotlib.pyplot as plt
from typing import Tuple, Optional


comp_idle = Id('Idle', [])
comp_burn = Id('Burn', [])


def idle_stage1_transition(prev: VehicleState, now: VehicleState, comp: CompState) -> Optional[Tuple[Optional[Action], CompState]]:
    """
    Fire first stage motor.
    """
    return Action.NEXT_STAGE, comp_burn


comp_idle.add_transition(idle_stage1_transition)

stage0 = Stage(area_m2=0.0, impulse_Ns=0.0, empty_mass_kg=5.0, engine_case_mass_kg=0.5, propellant_mass_kg=5.0,
               thrust_N=0.0, step_propellant_mass_kg=const(0.0), step_thrust_N=const(0.0))

stage1 = Stage(area_m2=1, impulse_Ns=700, empty_mass_kg=5.0, engine_case_mass_kg=0.5, propellant_mass_kg=5.0,
               thrust_N=11.0, step_propellant_mass_kg=linear(-0.5), step_thrust_N=const(11))

state = VehicleState(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

vehicle = Vehicle(comp_idle, stage0, 0, [stage0, stage1], None, state)

#########


dt = 0.1
end_time_s = 10.0
curr_time = 0.0

states = []

while curr_time < end_time_s:
    states.append(vehicle.state)
    vehicle = vehicle.step(dt)

    curr_time += dt

data = [s.dist_m for s in states]
plt.plot(data)
plt.show()
