# Point A is traveling along the x-axis, the distance it traveled at any time t is sin(t)+2*t.
# Point B is traveling along the x-axis too. The initial speed of point B is 1m/s, and the initial
# length of point B is zero.  The possible acceleration of Point B is between -4.5 to 4.5 m/s^2.
# You can change the acceleration of Point B at any time. Write a Python program to control Point B
# to make the distance between Point B and A as small as possible. The whole process lasts 500
# seconds. At the end, plot the difference between points A

import numpy as np
import matplotlib.pyplot as plt

# Constants
T = 500  # Total time
dt = 0.01  # Time step
num_steps = int(T / dt)

# Initialize variables
time = np.arange(0, T, dt)
pos_a = np.sin(0.1 * time) + np.sin(0.2 * time) + 1.5 * time
pos_b = np.zeros(num_steps)
speed_b = np.ones(num_steps)
accel_b = np.zeros(num_steps)

speed_b[0] = 1.0

# Control loop
for i in range(1, num_steps):
    error = pos_a[i - 1] - pos_b[i - 1]
    accel_b[i] = np.clip(error / dt, -4.5, 4.5)
    speed_b[i] = speed_b[i - 1] + accel_b[i] * dt
    pos_b[i] = pos_b[i - 1] + speed_b[i] * dt

# Calculate the difference between points A and B
distance_ab = (pos_a - pos_b)

# Plot the results
plt.plot(time, distance_ab, label='Distance between A and B')
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
#plt.legend(loc='center left', bbox_to_anchor=(0.6, 0.7))
plt.title('Distance between Points A and B over Time')
plt.show()
