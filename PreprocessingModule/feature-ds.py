import sys
import os
import json
import regex as re
from pathlib import Path

def create_feature_ds(json_file):
    # Function to create feature data structures from a JSON file
    features = {}
    data = json.load(json_file)
    count = 0
    
    # Loop through each key-value pair in the JSON file
    for key, value in data.items():
        if type(data[key]) is list:
            # If the value is a list, store the key as a feature
            features[count] = key
            count += 1
        else:
            # If the value is a dictionary, store each key as a sub-feature
            for k in value.keys():
                features[count] = {key : k}
                count += 1
    
    # Convert features to JSON format with indentation
    json_object = json.dumps(features, indent=6)
        
    # Get the result path and modify the name
    result = Path(json_file.name)
    name = re.sub('_DS.json','_features.json',result.name)
    
    # Define the path for the new feature JSON file
    path = sys.path[0] + '\\feature-data\\' + name
    
    # Write the JSON object to the new file
    with open(path, "w") as outfile:
        outfile.write(json_object)
        
    return name

def main():
    # Main function to create feature data structures for all JSON files in the specified directory
    print("Starting to create feature data structure...\n")
    path = sys.path[0] + '\\inverted-index-ds'
    json_files = [pos_json for pos_json in os.listdir(
        path) if pos_json.endswith('.json')]
    
    # Loop through each JSON file and create feature data structure
    for index, js in enumerate(json_files):
        with open(os.path.join(path, js)) as json_file:
            name = create_feature_ds(json_file)
            print(name + " has been successfully created")
    
    print("\nThe feature data structures of the files were successfully created")

if __name__ == "__main__":
    main()
