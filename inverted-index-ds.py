import sys
import os
import json
import regex as re
from pathlib import Path

def create_data_structures(json_file):
    # Function to create inverted index data structures from a JSON file
    inverted_index = {}
    data = json.load(json_file)
    word_len = 32
    dictionary_check = []
    item_ids = data.keys()
    
    # Loop through each item in the data
    for id in item_ids:
        item = data[id]
        keys_list = item.keys()
        for key in keys_list:
            # Check if the length of the item[key] is less than or equal to word_len
            if len(item[key]) <= word_len:
                # Check if the item[key] contains digits, "Yes", "No", or is already in dictionary_check
                if (bool(re.search(r'\d|Yes|No', item[key])) or item[key] in dictionary_check and key not in dictionary_check):
                    dictionary_check.append(key)
    
    dictionary_check = [*set(dictionary_check)]
                           
    # Loop through each item in the data again
    for id in item_ids:
        item = data[id]
        keys_list = item.keys()
        for key in keys_list:
            target_key = item[key].lower()
            target_key2 = "NoneType"
            if (key in dictionary_check):
                target_key = key.lower()
                target_key2 = item[key].lower()
            # Check if the length of target_key and target_key2 is less than or equal to word_len
            if len(target_key) <= word_len and len(target_key2) <= word_len:
                # Check if target_key2 is not "NoneType"
                if target_key2 != "NoneType":
                    # Check if target_key is in inverted_index.keys()
                    if target_key in inverted_index.keys():
                        key_level2 = inverted_index[target_key].keys()
                        # Check if target_key2 is in key_level2
                        if target_key2 in key_level2:
                            inverted_index[target_key][target_key2].append(id)
                        else:
                            inverted_index[target_key][target_key2] = [id]
                    else:
                        inverted_index[target_key] = {target_key2: [id]}              
                else:
                    # Check if target_key is in inverted_index.keys()
                    if target_key in inverted_index.keys():
                        inverted_index[target_key].append(id)
                    else:
                        inverted_index[target_key] = [id]

    # Convert inverted_index to JSON format with indentation
    json_object = json.dumps(inverted_index, indent=6)
        
    # Get the result path and modify the name
    result = Path(json_file.name)
    name = re.sub('.json','_DS.json',result.name)
    
    # Define the path for the new inverted index JSON file
    path = sys.path[0] + '\\inverted-index-ds\\' + name
    
    # Write the JSON object to the new file
    with open(path, "w") as outfile:
        outfile.write(json_object)
        
    return name


def main():
    # Main function to create inverted index data structures for all JSON files in the specified directory
    print("Starting to create inverted index data structure...\n")
    path = sys.path[0] + '\\data_with_ids'
    json_files = [pos_json for pos_json in os.listdir(
        path) if pos_json.endswith('.json')]
    
    # Loop through each JSON file and create inverted index data structure
    for index, js in enumerate(json_files):
        with open(os.path.join(path, js)) as json_file:
            name = create_data_structures(json_file)
            print(name + " has been successfully created")
    
    print("\nThe inverted index data structures of the files were successfully created")


if __name__ == "__main__":
    main()
