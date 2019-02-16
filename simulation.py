from rocket_sim.simulations import simulate
from vehicle_examples import single_stage, three_stage

vehicle, vehicle_name = three_stage()

simulation = simulate(vehicle, dt=0.1)

apogee_m, apogee_time_s = simulation.apogee
max_g_force, max_g_force_time_s = simulation.maximum_g_force

print(f'Apogee           (m):   {apogee_m}')
print(f'Time to apogee   (s):   {apogee_time_s}')
print(f'Time to land     (s):   {simulation.total_time - apogee_time_s}')
print(f'Time             (s):   {simulation.total_time}')
print(f'Impact Velocity  (m/s): {simulation.impact_velocity}')
print(f'Max G-force:            {max_g_force}')
print(f'Max G-force time (s):   {max_g_force_time_s}')


simulation.display_plots(vehicle_name)
