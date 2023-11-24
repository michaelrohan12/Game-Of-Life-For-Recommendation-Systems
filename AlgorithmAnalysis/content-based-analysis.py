import numpy as np
import json
import os
import time
import sys
import gc

def load_data(type_name):
    with open(os.path.join('inverted-index-ds', f'{type_name}_DS.json'), 'r') as file:
        item_id_data = json.load(file)
    return item_id_data

class ContentBasedRecommendation:
    def __init__(self, all_item_data):
        self.all_item_data = all_item_data

    def initialize_user_preferences(self):
    # Initialize user preferences randomly for each type and feature
        user_preferences = {}
    
        for type_name, item_data in self.all_item_data.items():
            user_preferences[type_name] = {}
            for feature, product_id_list in item_data.items():
                if isinstance(product_id_list, dict):
                    for sub_feature in product_id_list:
                        for product_id in product_id_list[sub_feature]:
                            if product_id not in user_preferences[type_name]:
                                user_preferences[type_name][product_id] = {}
                            user_preferences[type_name][product_id][(feature, sub_feature)] = np.random.rand()
                else:
                    for product_id in product_id_list:
                        if product_id not in user_preferences[type_name]:
                            user_preferences[type_name][product_id] = {}
                        user_preferences[type_name][product_id][feature] = np.random.rand()

        return user_preferences

    def content_based_recommendations(self, user_preferences, type_name, target_product_ids, n=5):
        # Content-based recommendation based on actual features
        all_features = set()
        available_products = list(user_preferences[type_name].keys())
        
        for target_product_id in target_product_ids:
            target_product_features = user_preferences[type_name][target_product_id]
            all_features.update(set(target_product_features.keys()))
            available_products.remove(target_product_id)  # Exclude the target product

        # Calculate similarity based on common features
        similarity_scores = []
        for product_id in available_products:
            product_features = user_preferences[type_name][product_id]
            common_features = set(product_features.keys()) & all_features
            similarity_score = len(common_features) / len(all_features)
            similarity_scores.append((product_id, similarity_score))

        # Sort products by similarity score
        similarity_scores.sort(key=lambda x: x[1], reverse=True)

        # Get top N similar products
        top_n_products = [product_id for product_id, _ in similarity_scores[:n]]

        return top_n_products

def analyze_time_and_space(num_simulations_list):
    all_types = ["Mobile", "Laptop", "CameraLens", "LaptopPeriferals", "Refrigerator", "TV", "Tablet", "WashingMachine", "WearableSmartDevice"]
    all_item_data = {type_name: load_data(type_name) for type_name in all_types}
    recommendation_system = ContentBasedRecommendation(all_item_data)

    for num_simulations in num_simulations_list:
        total_time = 0
        total_space = 0
        start_time = time.time()
        for _ in range(num_simulations):
            gc.collect()
            # Simulate user interactions for a single user and a single type
            user_preferences = recommendation_system.initialize_user_preferences()

            # Content-based recommendations
            target_type_name = "Mobile"
            target_product_ids = set(np.random.choice(list(user_preferences[target_type_name].keys()), 1600))
            
            recommendation_system.content_based_recommendations(user_preferences, target_type_name, target_product_ids)
            
            # Record space usage
            total_space += sys.getsizeof(target_product_ids)

            # Record time
        end_time = time.time()

        print(f"Ammortized Analysis - Number of Simulations: {num_simulations}\n")
        # Calculate and print amortized time
        amortized_time = (end_time - start_time) / num_simulations
        print(f'Averaged Time per Simulation: {amortized_time:.6f} seconds')

        # Calculate and print amortized space
        amortized_space = total_space / num_simulations
        print(f'Averaged Space per Simulation: {amortized_space:.6f} bytes\n\n\n')

if __name__ == "__main__":
    # Analyze time and space for a number of simulations
    num_simulations_list = [1, 5, 10, 50, 100]
    analyze_time_and_space(num_simulations_list)
