from rocket_sim.simulations import simulate
from rocket_sim.calculations import apogee, maximum_acceleration, g_force
from rocket_sim.graphics import time_series_plot_group
from vehicle_examples import single_stage, three_stage

vehicle, vehicle_name = three_stage()

states = simulate(vehicle, dt=0.1)

apogee_m, apogee_time_s = apogee(states)
impact_velocity_ms = states[-1].velocity_ms
max_accel_ms2, max_accel_time_s = maximum_acceleration(states)
total_time = states[-1].time_s

time = [s.time_s for s in states]
events = [(s.time_s, s.event) for s in states if s.event is not None]
events.append((apogee_time_s, 'Apogee'))


time_series_plot_group(vehicle_name, [
    (time, [s.mass_kg for s in states], events, 'Time (s)', 'Mass (kg)'),
    (time, [s.accel_ms2 for s in states], events, 'Time (s)', 'Acceleration (m/s2)'),
    (time, [s.velocity_ms for s in states], events, 'Time (s)', 'Velocity (m/s)'),
    (time, [s.dist_m for s in states], events, 'Time (s)', 'Altitude (m)'),
    (time, [s.thrust_N for s in states], events, 'Time (s)', 'Thrust (N)'),
    (time, [s.air_resistance_N for s in states], events, 'Time (s)', 'Air Resistance (N)'),
    ]
)


print(f'Apogee           (m):   {apogee_m}')
print(f'Time to apogee   (s):   {apogee_time_s}')
print(f'Time to land     (s):   {total_time - apogee_time_s}')
print(f'Time             (s):   {total_time}')
print(f'Impact Velocity  (m/s): {impact_velocity_ms}')
print(f'Max G-force:            {g_force(max_accel_ms2)}')
print(f'Max G-force time (s):   {max_accel_time_s}')
