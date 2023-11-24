import json
import os
import sys
from pathlib import Path

start = 1001  # Starting ID for items

def data_transformer(json_file):
    # Function to transform data by adding item IDs
    data = json.load(json_file)
    item_dict = {}

    global start  # Use the global starting ID

    # Create a list of IDs from the starting point to 20000
    ids = [format(x, '02d') for x in list(range(start, 20000))]

    for i in range(len(data)):
        # Remove the existing "id" field from the data
        del data[i]["id"]

        # Add the transformed data with the new item ID
        item_dict[ids[i]] = data[i]

    # Update the starting ID for the next iteration
    start = int(ids[i+1])
    
    # Convert the transformed data to JSON format with indentation
    json_object = json.dumps(item_dict, indent=4)

    # Get the result path
    result = Path(json_file.name)

    # Define the path for the new transformed JSON file
    path = sys.path[0] + '\\data_with_ids\\' + result.name
    
    # Write the JSON object to the new file
    with open(path, "w") as outfile:
        outfile.write(json_object)
        
    return result.name

def main():
    # Main function to transform data in all JSON files in the specified directory
    print("Starting to initialize the IDs...\n")
    path = sys.path[0] + '\\data'
    json_files = [pos_json for pos_json in os.listdir(
        path) if pos_json.endswith('.json')]
    
    # Loop through each JSON file and transform the data
    for index, js in enumerate(json_files):
        with open(os.path.join(path, js)) as json_file:
            name = data_transformer(json_file)
            print(name + " has been successfully initialized with item IDs")
    
    print("\nAll the files were successfully transformed.")

if __name__ == "__main__":
    main()
