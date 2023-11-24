import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

def load_data(type_name):
    with open(os.path.join('inverted-index-ds', f'{type_name}_DS.json'), 'r') as file:
        item_id_data = json.load(file)
    return item_id_data

def initialize_user_preferences(all_item_data):
    # Initialize user preferences randomly for each type and feature
    user_preferences = {}
    for type_name, item_data in all_item_data.items():
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

def simulate_user_interactions(user_preferences, user_id, type_name):
    # Simulate user interactions with a type of e-commerce
    product_ids = list(user_preferences[type_name].keys())
    
    # Randomly select some products that the user interacts with
    interacted_products = np.random.choice(product_ids, size=np.random.randint(1, len(product_ids)), replace=False)

    for product_id in interacted_products:
        # Simulate user ratings (random for demonstration)
        user_preferences[type_name][product_id][f'user_{user_id}_rating'] = np.random.rand()

    return user_preferences

def calculate_similarity(user_preferences, type_name):
    # Calculate similarity matrix between products for the specified type
    product_ids = list(user_preferences[type_name].keys())
    max_features = max(len(user_preferences[type_name][product_id]) for product_id in product_ids)

    product_matrix = []

    for product_id in product_ids:
        user_preferences_values = user_preferences[type_name][product_id].values()
        numeric_values = [val for val in user_preferences_values if isinstance(val, (int, float))]
        padded_values = numeric_values + [0.0] * (max_features - len(numeric_values))
        product_matrix.append(padded_values)

    product_matrix = np.array(product_matrix, dtype=np.float64)
    similarity_matrix = cosine_similarity(product_matrix, product_matrix)
    return product_ids, similarity_matrix

def get_top_n_similar_products(user_preferences, user_id, type_name, n=5):
    # Get the top N similar products based on user interactions
    product_ids, similarity_matrix = calculate_similarity(user_preferences, type_name)

    # Extract user ratings for the specified user
    user_ratings = [user_preferences[type_name][product_id].get(f'user_{user_id}_rating', 0.0) for product_id in product_ids]

    target_product_index = np.argmax(user_ratings)
    similar_products_indices = np.argsort(similarity_matrix[target_product_index])[::-1][:n]

    return [product_ids[i] for i in similar_products_indices]

# Load data for all types
all_types = ["Mobile", "Laptop", "CameraLens", "LaptopPeriferals", "Refrigerator", "TV", "Tablet", "WashingMachine", "WearableSmartDevice"]
all_item_data = {}
for type_name in all_types:
    item_id_data = load_data(type_name)
    all_item_data[type_name] = item_id_data

# Initialize user preferences
user_preferences = initialize_user_preferences(all_item_data)

# Simulate user interactions for a single user and a single type
target_user_id = np.random.randint(1001, 2001)  # Replace with the desired user ID within the specified range
type_name = "Mobile"  # Replace with the desired type

user_preferences = simulate_user_interactions(user_preferences, target_user_id, type_name)

# Generate recommendations for the simulated user
recommendations = get_top_n_similar_products(user_preferences, target_user_id, type_name)
print(f"Recommendations for user {target_user_id} in type {type_name}:", recommendations)
