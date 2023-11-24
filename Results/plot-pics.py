import matplotlib.pyplot as plt
import numpy as np

# Time values for collaborative filtering, content-based, and game of life
cf_times = [0.141838, 0.140213, 0.141601, 0.148111, 0.160513]
cb_times = [0.100080, 0.115311, 0.116601, 0.114269, 0.115816]
gol_times = [0.098094, 0.070598, 0.063523, 0.072811, 0.073013]

# Number of users
num_users_list = [1, 5, 10, 50, 100]

# Bar width
bar_width = 0.25

# Set up positions for the bars
bar_positions_cf = np.arange(len(num_users_list))
bar_positions_cb = bar_positions_cf + bar_width
bar_positions_gol = bar_positions_cb + bar_width

# Plotting the bar graph
plt.figure(figsize=(10, 6))

plt.bar(bar_positions_cf, cf_times, width=bar_width, label='Collaborative Filtering', align='center')
plt.bar(bar_positions_cb, cb_times, width=bar_width, label='Content-Based', align='center')
plt.bar(bar_positions_gol, gol_times, width=bar_width, label='Game of Life', align='center')

# Set x-axis labels
plt.xticks(bar_positions_cb, num_users_list)

plt.title('Recommendation System Comparison', weight='bold')
plt.xlabel('Number of Users', weight='bold')
plt.ylabel('Time (seconds)', weight='bold')
plt.legend()
plt.grid(axis='y')
plt.show()
