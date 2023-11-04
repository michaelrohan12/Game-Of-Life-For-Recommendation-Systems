import sys
import os
import json
import regex as re
from pathlib import Path

def create_feature_ds(json_file):
    features = {}
    data = json.load(json_file)
    count = 0
    
    for key, value in data.items():
        if type(data[key]) is list:
            features[count] = key
            count += 1
        else:
            for k in value.keys():
                features[count] = {key : k}
                count += 1
    
    json_object = json.dumps(features, indent=6)
        
    result = Path(json_file.name)
    
    name = re.sub('_DS.json','_features.json',result.name)
    
    path = sys.path[0] + '\\feature-data\\' + name
    
    with open(path, "w") as outfile:
        outfile.write(json_object)
        
    return name


def main():
    print("Starting to create feature data structure...\n")
    path = sys.path[0] + '\\inverted-index-ds'
    json_files = [pos_json for pos_json in os.listdir(
        path) if pos_json.endswith('.json')]
    for index, js in enumerate(json_files):
        with open(os.path.join(path, js)) as json_file:
            name = create_feature_ds(json_file)
            print(name + " has been successfully created")
    print("\nThe feature data structures of the files were successfully created")


if __name__ == "__main__":
    main()
