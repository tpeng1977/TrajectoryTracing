import numpy as np
import random

np.random.seed(1024)
# 平均每小时进入 60 辆车，计算平均时间间隔
mean_interval = 3600 / 60
intervals = []

# 生成指数分布的时间间隔
while sum(intervals) < 3600:
    interval = np.random.exponential(mean_interval) + 0.35
    intervals.append(interval)

min_interval = min(intervals)
print(f"min_interval: {min_interval}")
# 计算车辆进入时间
entry_times = [sum(intervals[:i]) for i in range(1, len(intervals)+1)]

print("一小时内车辆的模拟进入时间：")
for time in entry_times:
    print(f"{time} 秒")


import matplotlib.pyplot as plt

# Generate x values
x = np.linspace(0, 2 * np.pi, 1000)

# Calculate y values
y1 = np.sin(x)
y2 = np.sin(x) - 0.5

# Create the plot
plt.plot(x, y1, label='y = sin(x)', color='red', alpha=0.4)
plt.plot(x, y2, label='y = sin(x) - 0.5', color='red', alpha=1.0)

# Fill the area between the curves
plt.fill_between(x, y1, y2, where=(y1 > y2), color='red', alpha=0.1)

# Add labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Area between y = sin(x) and y = sin(x) - 0.5')
plt.legend()

# Show the plot
plt.show()


