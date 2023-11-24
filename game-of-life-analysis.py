import time
import gc
import numpy as np
import json
import os
import sys
import random

class GameOfLife:
    def __init__(self, grid_width, grid_height):
        # Constructor to initialize the GameOfLife object
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cells = self.initialize_cells()

    def initialize_cells(self):
        # Method to initialize cells with random product IDs
        cells = np.zeros((self.grid_height, self.grid_width), dtype=np.dtype(
            [('product_id', int), ('value', int)]))

        with open(os.path.join('feature-data', 'Mobile_features.json'), 'r') as file:
            sample_data = json.load(file)

        with open(os.path.join('inverted-index-ds', 'Mobile_DS.json'), 'r') as file:
            item_id_data = json.load(file)

        for row in range(self.grid_height):
            key = str(row)
            if type(sample_data[key]) is dict:
                idx1 = list(sample_data[key].keys())[0]
                idx2 = list(sample_data[key].values())[0]
                product_ids = item_id_data[idx1][idx2]
            else:
                product_ids = item_id_data[sample_data[key]]
            for col in range(self.grid_width):
                cells[row, col] = (random.choice(product_ids), 0)

        return cells

    def update_cells(self):
        # Method to update cells based on the Game of Life rules
        updated_cells = np.zeros((self.cells.shape[0], self.cells.shape[1]), dtype=np.dtype(
            [('product_id', int), ('value', int)]))

        for row in range(self.cells.shape[0]):
            for col in range(self.cells.shape[1]):
                updated_cells[row, col] = (self.cells[row, col]['product_id'], 0)

        for row, col in np.ndindex(self.cells.shape):
            neighborhood = self.cells[max(row - 1, 0):min(row + 2, self.cells.shape[0]),
                                max(col - 1, 0):min(col + 2, self.cells.shape[1])]
            alive = np.sum(neighborhood['value'])
        

            if self.cells[row, col]['value'] == 1:
                if alive < 2 or alive > 3:
                    continue
                elif 2 <= alive <= 3:
                    updated_cells[row, col]['value'] = 1
            else:
                if alive == 3:
                    updated_cells[row, col]['value'] = 1

        return updated_cells

    def perform_user_interactions(self, num_interactions):
        # Method to simulate user interactions by setting random cells to alive
        for _ in range(num_interactions):
            row = random.randint(0, self.grid_height - 1)
            col = random.randint(0, self.grid_width - 1)
            self.cells[row, col]['value'] = 1

    def generate_recommendations(self, interactions_per_user, max_iterations=100):
        # Method to generate recommendations using the Game of Life algorithm
        previous_state = None
        self.perform_user_interactions(interactions_per_user)

        for _ in range(max_iterations):

            # Update cells based on the Game of Life rules
            self.cells = self.update_cells()

            # Check for stability
            current_state = tuple(map(tuple, self.cells))
            if current_state == previous_state:
                break

            previous_state = current_state

def perform_amortized_analysis(num_users, interactions_per_user):
    # Function to perform amortized analysis
    grid_width = 80
    grid_height = 60
    total_time = 0
    total_space = 0

    for _ in range(num_users):
        gc.collect()
        game = GameOfLife(grid_width, grid_height)
        total_space += sys.getsizeof(game.cells['product_id'][game.cells['value'] != 0])
        # Simulate user interactions and update cells
        start_time = time.time()
        game.generate_recommendations(interactions_per_user)
        end_time = time.time()
        chosen_product_ids = set()
        for cell in game.cells:
            for value in cell:
                if value[1] != 0:
                    chosen_product_ids.add(value[0])
                    if len(chosen_product_ids) == 5:
                        break
        total_time += end_time - start_time
        

    print(f"Ammortized Analysis - Number of Simulations: {num_users}\n")
    # Calculate and print amortized time
    amortized_time = total_time / num_users
    print(f'Averaged Time per Simulation: {amortized_time:.6f} seconds')

    # Calculate and print amortized space
    amortized_space = total_space / num_users
    print(f'Averaged Space per Simulation: {amortized_space:.6f} bytes\n\n\n')

def main():
    # Main function to perform amortized analysis for different numbers of users
    num_users_list = [1, 5, 10, 50, 100]
    interactions_per_user = 50

    for num_users in num_users_list:
        perform_amortized_analysis(num_users, interactions_per_user)

if __name__ == "__main__":
    main()
