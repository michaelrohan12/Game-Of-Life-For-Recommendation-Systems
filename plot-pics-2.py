import matplotlib.pyplot as plt
import numpy as np

# Memory values for collaborative filtering, content-based, and game of life (in bytes)
cf_memory = [272, 0, 0]
cb_memory = [0, 32984, 0]  # Replace with actual values for content-based
gol_memory = [0, 0, 112]  # Replace with actual values for game of life

# Recommendation system types
recommendation_types = ['Collaborative Filtering', 'Content-Based', 'Game of Life']

# Bar width
bar_width = 0.25

# Set up positions for the bars
bar_positions = np.arange(len(recommendation_types))

# Plotting the bar graph with a logarithmic y-axis
plt.figure(figsize=(10, 6))

plt.bar(bar_positions + bar_width*0.001, cf_memory, width=bar_width, label='Collaborative Filtering')
plt.bar(bar_positions, cb_memory, width=bar_width, label='Content-Based')
plt.bar(bar_positions - bar_width*0.001, gol_memory, width=bar_width, label='Game of Life')

# Set x-axis labels
plt.xticks(bar_positions, recommendation_types)

# Set logarithmic scale on y-axis
plt.yscale('log')

plt.title('Memory Consumption of Recommendation Systems', weight='bold')
plt.xlabel('Recommendation System Type', weight='bold')
plt.ylabel('Memory (bytes) - Logarithmic Scale', weight='bold')
plt.legend()
plt.grid(axis='y', which='both', linestyle='--', linewidth=0.5)
plt.show()
